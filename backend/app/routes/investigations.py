from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from app.db.database import get_db
from app.models.investigation import (
    DBInvestigation,
    InvestigationCreate,
    InvestigationStart,
    InvestigationResponse,
    InvestigationStatus,
)
from app.services.planner import plan_mission
from app.services.calle_adapter import get_calle_adapter
from app.services.analyzer import analyze_transcript

router = APIRouter()

# In-memory mapping of investigation_id to telephony call_id
_active_calls = {}

def db_to_response(db_item: DBInvestigation) -> InvestigationResponse:
    return InvestigationResponse(
        id=db_item.id,
        mission=db_item.mission,
        status=db_item.status,
        target_name=db_item.target_name,
        phone_number=db_item.phone_number,
        planned_questions=db_item.planned_questions or [],
        summary=db_item.summary,
        answers=db_item.answers or [],
        duration_seconds=db_item.duration_seconds or 0,
        hold_seconds=db_item.hold_seconds or 0,
        representative=db_item.representative,
        timestamp=db_item.timestamp.isoformat() if db_item.timestamp else datetime.now(timezone.utc).isoformat(),
        transcript=db_item.transcript or [],
        recording_url=db_item.recording_url,
        calle_call_id=db_item.calle_call_id,
        created_at=db_item.created_at.isoformat() if db_item.created_at else datetime.now(timezone.utc).isoformat(),
        updated_at=db_item.updated_at.isoformat() if db_item.updated_at else datetime.now(timezone.utc).isoformat(),
    )

@router.post("/investigations", response_model=InvestigationResponse, status_code=status.HTTP_201_CREATED)
def create_investigation(
    payload: InvestigationCreate,
    db: Session = Depends(get_db)
):
    plan_data = plan_mission(payload.mission)
    target_name = plan_data.get("target_name")
    phone_number = plan_data.get("phone_number")
    planned_questions = plan_data.get("planned_questions", [])
    confidence = plan_data.get("target_confidence", "low")

    # LOCKED DECISION #1: If target/phone cannot be confidently identified, ask user to confirm/provide phone number
    if confidence == "low" or not phone_number or not target_name:
        status_val = InvestigationStatus.NEEDS_USER_INPUT.value
    else:
        status_val = InvestigationStatus.READY.value

    db_item = DBInvestigation(
        mission=payload.mission,
        status=status_val,
        target_name=target_name,
        phone_number=phone_number,
        planned_questions=planned_questions,
        answers=[],
        transcript=[],
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_to_response(db_item)

@router.post("/investigations/{investigation_id}/start", response_model=InvestigationResponse)
def start_investigation(
    investigation_id: str,
    payload: InvestigationStart = None,
    db: Session = Depends(get_db)
):
    db_item = db.query(DBInvestigation).filter(DBInvestigation.id == investigation_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Investigation not found")
    
    if payload:
        if payload.phone_number:
            db_item.phone_number = payload.phone_number
        if payload.target_name:
            db_item.target_name = payload.target_name

    # Initialize telephony adapter with error handling
    try:
        calle = get_calle_adapter()
    except (ValueError, ImportError) as err:
        # Adapter initialization failed – mark investigation as failed
        db_item.status = InvestigationStatus.FAILED.value
        db_item.summary = f"Adapter init failed: {str(err)}"
        db.commit()
        db.refresh(db_item)
        return db_to_response(db_item)

    # Start the CALL-E call with error handling
    try:
        call_res = calle.start_call(
            phone_number=db_item.phone_number,
            target_name=db_item.target_name or "Target Line",
            questions=db_item.planned_questions or []
        )
    except Exception as err:
        # start_call raised an exception – mark investigation as failed
        db_item.status = InvestigationStatus.FAILED.value
        db_item.summary = f"CALL-E start_call exception: {str(err)}"
        db.commit()
        db.refresh(db_item)
        return db_to_response(db_item)

    # If the CALL-E response indicates failure, handle it
    if call_res.get("status") == "failed":
        db_item.status = InvestigationStatus.FAILED.value
        db_item.summary = call_res.get("message", "Call initiation failed")
        db.commit()
        db.refresh(db_item)
        return db_to_response(db_item)

    # Normal successful start – persist call IDs and update status
    call_id = call_res["call_id"]
    _active_calls[db_item.id] = call_id

    # Persist the CALL-E call task ID for polling and event retrieval
    calle_call_id = call_res.get("calle_call_id")
    if calle_call_id:
        db_item.calle_call_id = calle_call_id

    db_item.status = InvestigationStatus.DIALING.value
    db.commit()
    db.refresh(db_item)
    return db_to_response(db_item)

@router.get("/investigations/{investigation_id}", response_model=InvestigationResponse)
def get_investigation(
    investigation_id: str,
    db: Session = Depends(get_db)
):
    db_item = db.query(DBInvestigation).filter(DBInvestigation.id == investigation_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Investigation not found")

    # Poll telephony adapter if call is active
    if db_item.id in _active_calls:
        call_id = _active_calls[db_item.id]
        calle = get_calle_adapter()
        call_status = calle.get_call_status(call_id)
        
        new_status = call_status.get("status", db_item.status)
        db_item.status = new_status
        db_item.transcript = call_status.get("transcript", db_item.transcript)
        db_item.duration_seconds = call_status.get("duration_seconds", db_item.duration_seconds)
        db_item.hold_seconds = call_status.get("hold_seconds", db_item.hold_seconds)
        
        if "representative" in call_status:
            db_item.representative = call_status["representative"]
        if "recording_url" in call_status:
            db_item.recording_url = call_status["recording_url"]

        if new_status == InvestigationStatus.COMPLETED.value and not db_item.answers:
            # Perform Gemini transcript analysis
            analysis = analyze_transcript(db_item.planned_questions, db_item.transcript)
            db_item.summary = analysis.get("summary")
            db_item.answers = analysis.get("answers", [])
            if analysis.get("representative"):
                db_item.representative = analysis.get("representative")

        db.commit()
        db.refresh(db_item)

    return db_to_response(db_item)

@router.get("/investigations", response_model=List[InvestigationResponse])
def list_investigations(
    db: Session = Depends(get_db)
):
    items = db.query(DBInvestigation).order_by(DBInvestigation.created_at.desc()).all()
    return [db_to_response(item) for item in items]

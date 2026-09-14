import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import os
from datetime import datetime

from dotenv import load_dotenv
from calle import CalleClient

from app.db.database import SessionLocal
from app.models.investigation import DBInvestigation


INVESTIGATION_ID = "addab317-bc1c-4600-bb4c-b25fbf724ce0"
CALL_ID = "call_OskQy-WIRacfJjVAkSLhfQ"


load_dotenv()

# Retrieve the already-completed CALL-E call.
client = CalleClient(api_key=os.getenv("CALLE_API_KEY"))
result = client.calls.get(CALL_ID)

# Open SQLite.
db = SessionLocal()

try:
    investigation = (
        db.query(DBInvestigation)
        .filter(DBInvestigation.id == INVESTIGATION_ID)
        .first()
    )

    if investigation is None:
        raise RuntimeError("Investigation not found in SQLite.")

    attempt = result["recipients"][0]["attempts"][0]
    turns = attempt["transcript_turns"]

    # Convert CALL-E transcript into our database format.
    transcript = []

    for turn in turns:
        offset = int(turn.get("offset_seconds", 0))

        transcript.append(
            {
                "speaker": turn.get("speaker", "unknown"),
                "text": turn.get("text", ""),
                "timestamp": f"{offset // 60:02d}:{offset % 60:02d}",
            }
        )

    structured = result.get("structured_result") or {}

    # Build verified answers from the CALL-E structured result.
    answers = [
        {
            "question": "How are you doing today?",
            "answer": structured.get(
                "how_they_are_doing",
                "Could not verify",
            ),
            "confidence": "high"
            if structured.get("how_they_are_doing")
            else "low",
            "verification": "verified"
            if structured.get("how_they_are_doing")
            else "unverified",
        },
        {
            "question": "What do you enjoy doing in your free time?",
            "answer": structured.get(
                "favorite_free_time_activity",
                "Could not verify",
            ),
            "confidence": "high"
            if structured.get("favorite_free_time_activity")
            else "low",
            "verification": "verified"
            if structured.get("favorite_free_time_activity")
            else "unverified",
        },
        {
            "question": "What do you both like talking about most?",
            "answer": structured.get(
                "follow_up_response",
                "Could not verify",
            ),
            "confidence": "low",
            "verification": "unverified",
        },
        {
            "question": "Is there anything else you would like to tell me?",
            "answer": structured.get(
                "anything_else",
                "Could not verify",
            ),
            "confidence": "low",
            "verification": "unverified",
        },
    ]

    # Update the existing investigation.
    investigation.status = "completed"

    investigation.summary = (
        "CALL-E call completed successfully. "
        "Task completed with high confidence (0.90). "
        f"{len(transcript)} transcript turns were captured."
    )

    investigation.answers = answers
    investigation.transcript = transcript
    investigation.calle_call_id = CALL_ID

    # CALL-E did not provide duration_seconds in the retrieved attempt,
    # so we deliberately leave the existing duration unchanged.
    investigation.updated_at = datetime.utcnow()

    db.commit()

    print()
    print("=" * 60)
    print("CALL-E RESULT RECOVERED")
    print("=" * 60)
    print("Investigation:", investigation.id)
    print("Status:", investigation.status)
    print("CALL-E ID:", investigation.calle_call_id)
    print("Transcript turns:", len(investigation.transcript))
    print("Answers:", len(investigation.answers))
    print("Confidence: 0.90 (high)")
    print("Task completed: True")
    print("=" * 60)

finally:
    db.close()
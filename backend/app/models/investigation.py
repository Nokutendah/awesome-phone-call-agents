from sqlalchemy import Column, String, Integer, Text, DateTime, JSON
from sqlalchemy.sql import func
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from enum import Enum
import uuid
import datetime
from app.db.database import Base

class InvestigationStatus(str, Enum):
    DRAFT = "draft"
    READY = "ready"
    DIALING = "dialing"
    IVR = "ivr"
    HOLDING = "holding"
    SPEAKING = "speaking"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"
    NEEDS_USER_INPUT = "needs_user_input"

class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class VerificationState(str, Enum):
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    NOT_ANSWERED = "not_answered"
    CONTRADICTED = "contradicted"

class QuestionAnswerSchema(BaseModel):
    question: str
    answer: str
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    verification: VerificationState = VerificationState.UNVERIFIED

class TranscriptItemSchema(BaseModel):
    speaker: str
    text: str
    timestamp: str

# SQLAlchemy Model
class DBInvestigation(Base):
    __tablename__ = "investigations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    mission = Column(Text, nullable=False)
    status = Column(String, nullable=False, default=InvestigationStatus.DRAFT.value)
    target_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    planned_questions = Column(JSON, default=list)
    summary = Column(Text, nullable=True)
    answers = Column(JSON, default=list)
    representative = Column(String, nullable=True)
    duration_seconds = Column(Integer, default=0)
    hold_seconds = Column(Integer, default=0)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    transcript = Column(JSON, default=list)
    recording_url = Column(String, nullable=True)
    calle_call_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

# Pydantic Request/Response Schemas
class InvestigationCreate(BaseModel):
    mission: str

class InvestigationStart(BaseModel):
    phone_number: Optional[str] = None
    target_name: Optional[str] = None

class InvestigationResponse(BaseModel):
    id: str
    mission: str
    status: str
    target_name: Optional[str] = None
    phone_number: Optional[str] = None
    planned_questions: List[str] = []
    summary: Optional[str] = None
    answers: List[QuestionAnswerSchema] = []
    duration_seconds: int = 0
    hold_seconds: int = 0
    representative: Optional[str] = None
    timestamp: str
    transcript: List[TranscriptItemSchema] = []
    recording_url: Optional[str] = None
    calle_call_id: Optional[str] = None
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


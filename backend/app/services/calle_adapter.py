from abc import ABC, abstractmethod
from typing import Dict, Any, List
import time
import uuid
import datetime
from app.config import get_settings

settings = get_settings()

class AbstractCalleAdapter(ABC):
    @abstractmethod
    def start_call(self, phone_number: str, target_name: str, questions: List[str]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_call_status(self, call_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def hangup(self, call_id: str) -> Dict[str, Any]:
        pass

# In-memory session state store for Telephony Engine
_mock_calls: Dict[str, Dict[str, Any]] = {}

class MockCalleAdapter(AbstractCalleAdapter):
    """
    Mock implementation of CALL-E Telephony Engine.
    Simulates real-world call flow: dialing -> IVR phone tree navigation -> holding -> representative speaking -> completed.
    """
    def start_call(self, phone_number: str, target_name: str, questions: List[str]) -> Dict[str, Any]:
        call_id = f"calle_{uuid.uuid4().hex[:10]}"
        start_time = time.time()

        _mock_calls[call_id] = {
            "call_id": call_id,
            "phone_number": phone_number,
            "target_name": target_name or "Business Line",
            "questions": questions,
            "start_time": start_time,
            "representative": "Sarah (Customer Specialist)",
            "hold_seconds": 6,
            "recording_url": f"https://calle.ai/recordings/{call_id}.mp3",
        }

        return {
            "call_id": call_id,
            "status": "dialing",
            "message": f"Dialing {phone_number}..."
        }

    def get_call_status(self, call_id: str) -> Dict[str, Any]:
        if call_id not in _mock_calls:
            return {"status": "failed", "message": "Call ID not found"}

        data = _mock_calls[call_id]
        elapsed = time.time() - data["start_time"]

        target = data["target_name"]
        questions = data["questions"]
        q1 = questions[0] if len(questions) > 0 else "Do you offer wedding cake services?"
        q2 = questions[1] if len(questions) > 1 else "What is your typical advance notice lead time?"

        if elapsed < 3:
            return {
                "call_id": call_id,
                "status": "dialing",
                "message": f"Ringing line at {data['phone_number']}...",
                "transcript": [],
                "duration_seconds": int(elapsed),
                "hold_seconds": 0,
            }
        elif elapsed < 8:
            return {
                "call_id": call_id,
                "status": "ivr",
                "message": "Connected to IVR phone tree. Sending DTMF 1 for Customer Support...",
                "transcript": [
                    {"speaker": "IVR System", "text": f"Thank you for calling {target}. Press 1 for Store Inquiries, or 2 for Bakery counter.", "timestamp": "00:04"},
                    {"speaker": "CallBot AI", "text": "[DTMF Tone: 1]", "timestamp": "00:06"},
                ],
                "duration_seconds": int(elapsed),
                "hold_seconds": 0,
            }
        elif elapsed < 14:
            return {
                "call_id": call_id,
                "status": "holding",
                "message": "Transferring call to representative... Elevator music playing.",
                "transcript": [
                    {"speaker": "IVR System", "text": f"Thank you for calling {target}. Press 1 for Store Inquiries, or 2 for Bakery counter.", "timestamp": "00:04"},
                    {"speaker": "CallBot AI", "text": "[DTMF Tone: 1]", "timestamp": "00:06"},
                    {"speaker": "System", "text": "[Call put on hold - Hold Music Playing]", "timestamp": "00:08"},
                ],
                "duration_seconds": int(elapsed),
                "hold_seconds": int(elapsed - 8),
            }
        elif elapsed < 25:
            return {
                "call_id": call_id,
                "status": "speaking",
                "message": f"Speaking live with representative {data['representative']}...",
                "transcript": [
                    {"speaker": "IVR System", "text": f"Thank you for calling {target}. Press 1 for Store Inquiries, or 2 for Bakery counter.", "timestamp": "00:04"},
                    {"speaker": "CallBot AI", "text": "[DTMF Tone: 1]", "timestamp": "00:06"},
                    {"speaker": "System", "text": "[Call put on hold - Hold Music Playing]", "timestamp": "00:08"},
                    {"speaker": "Representative Sarah", "text": f"Hi, thanks for calling {target}! My name is Sarah. How can I help you today?", "timestamp": "00:14"},
                    {"speaker": "CallBot AI", "text": f"Hello Sarah! I am CallBot, an AI assistant calling on behalf of a customer. Could you tell me: {q1}", "timestamp": "00:16"},
                    {"speaker": "Representative Sarah", "text": "Yes, absolutely! We do bake gluten-free wedding cakes upon request, prepared in a dedicated sanitized workstation.", "timestamp": "00:20"},
                    {"speaker": "CallBot AI", "text": f"That's great! And also, {q2}", "timestamp": "00:22"},
                    {"speaker": "Representative Sarah", "text": "We usually recommend ordering at least 3 weeks in advance during peak season.", "timestamp": "00:24"},
                ],
                "duration_seconds": int(elapsed),
                "hold_seconds": 6,
            }
        elif elapsed < 28:
            return {
                "call_id": call_id,
                "status": "analyzing",
                "message": "Call completed successfully. AI engine analyzing transcript and extracting answers...",
                "transcript": [
                    {"speaker": "IVR System", "text": f"Thank you for calling {target}. Press 1 for Store Inquiries, or 2 for Bakery counter.", "timestamp": "00:04"},
                    {"speaker": "CallBot AI", "text": "[DTMF Tone: 1]", "timestamp": "00:06"},
                    {"speaker": "System", "text": "[Call put on hold - Hold Music Playing]", "timestamp": "00:08"},
                    {"speaker": "Representative Sarah", "text": f"Hi, thanks for calling {target}! My name is Sarah. How can I help you today?", "timestamp": "00:14"},
                    {"speaker": "CallBot AI", "text": f"Hello Sarah! I am CallBot, an AI assistant calling on behalf of a customer. Could you tell me: {q1}", "timestamp": "00:16"},
                    {"speaker": "Representative Sarah", "text": "Yes, absolutely! We do bake gluten-free wedding cakes upon request, prepared in a dedicated sanitized workstation.", "timestamp": "00:20"},
                    {"speaker": "CallBot AI", "text": f"That's great! And also, {q2}", "timestamp": "00:22"},
                    {"speaker": "Representative Sarah", "text": "We usually recommend ordering at least 3 weeks in advance during peak season.", "timestamp": "00:24"},
                    {"speaker": "CallBot AI", "text": "Thank you so much for the detailed information, Sarah! Have a wonderful day.", "timestamp": "00:26"},
                    {"speaker": "Representative Sarah", "text": "You too! Bye bye.", "timestamp": "00:27"},
                ],
                "duration_seconds": 28,
                "hold_seconds": 6,
            }
        else:
            return {
                "call_id": call_id,
                "status": "completed",
                "message": "Call completed and analyzed.",
                "representative": data["representative"],
                "recording_url": data["recording_url"],
                "duration_seconds": 28,
                "hold_seconds": 6,
                "transcript": [
                    {"speaker": "IVR System", "text": f"Thank you for calling {target}. Press 1 for Store Inquiries, or 2 for Bakery counter.", "timestamp": "00:04"},
                    {"speaker": "CallBot AI", "text": "[DTMF Tone: 1]", "timestamp": "00:06"},
                    {"speaker": "System", "text": "[Call put on hold - Hold Music Playing]", "timestamp": "00:08"},
                    {"speaker": "Representative Sarah", "text": f"Hi, thanks for calling {target}! My name is Sarah. How can I help you today?", "timestamp": "00:14"},
                    {"speaker": "CallBot AI", "text": f"Hello Sarah! I am CallBot, an AI assistant calling on behalf of a customer. Could you tell me: {q1}", "timestamp": "00:16"},
                    {"speaker": "Representative Sarah", "text": "Yes, absolutely! We do bake gluten-free wedding cakes upon request, prepared in a dedicated sanitized workstation.", "timestamp": "00:20"},
                    {"speaker": "CallBot AI", "text": "That's great! And also, " + q2, "timestamp": "00:22"},
                    {"speaker": "Representative Sarah", "text": "We usually recommend ordering at least 3 weeks in advance during peak season.", "timestamp": "00:24"},
                    {"speaker": "CallBot AI", "text": "Thank you so much for the detailed information, Sarah! Have a wonderful day.", "timestamp": "00:26"},
                    {"speaker": "Representative Sarah", "text": "You too! Bye bye.", "timestamp": "00:27"},
                ],
            }

    def hangup(self, call_id: str) -> Dict[str, Any]:
        if call_id in _mock_calls:
            _mock_calls[call_id]["forced_end"] = True
        return {"call_id": call_id, "status": "completed", "message": "Call terminated by user."}

class RealCalleAdapter(AbstractCalleAdapter):
    """
    Real CALL-E Telephony Engine Adapter using official Python SDK `calle-ai`.
    Docs: https://docs.heycall-e.com/calls

    Architecture: Asynchronous create + poll flow.
      1. calls.create()         → returns call task ID immediately
      2. calls.get(call_id)     → read current state (polling)
      3. calls.wait_for_result() → block until terminal state
      4. calls.list_events()    → ordered lifecycle event trace

    SDK method signatures (from calle-ai v0.7.0):
      create(*, task, recipients=None, result_schema=None, recipient_result_schema=None,
             metadata=None, webhook_url=None, idempotency_key=None) -> dict
      get(call_id: str) -> dict
      wait_for_result(call_id, *, interval_seconds=2.0, timeout_seconds=600.0) -> dict
      list_events(call_id, *, cursor=None, limit=None) -> dict
    """

    # Terminal statuses indicating the call is finished
    TERMINAL_STATUSES = {"completed", "failed", "canceled", "declined", "error"}

    def __init__(self, api_key: str, client: Any = None):
        if not api_key and not client:
            raise ValueError(
                "CALLE_MODE is set to 'real', but CALLE_API_KEY is missing in backend configuration. "
                "Please set CALLE_API_KEY in your environment or set CALLE_MODE=mock."
            )
        self.api_key = api_key
        if client:
            self.client = client
        else:
            try:
                from calle import CalleClient
                self.client = CalleClient(api_key=api_key)
            except ImportError:
                raise ImportError("The 'calle-ai' Python SDK package is not installed. Please run `pip install calle-ai`.")

        # Internal store: maps our internal call_id -> call metadata
        self._calls: Dict[str, Dict[str, Any]] = {}

    def _build_task_instruction(self, phone_number: str, target_name: str, questions: List[str]) -> str:
        """Build the natural-language task instruction for CALL-E."""
        return (
            f"Call target business '{target_name}' at {phone_number}. "
            f"Identify clearly as CallBot, an AI assistant calling on behalf of a customer inquiring about business information. "
            f"Ask the following specific questions:\n" + "\n".join(f"- {q}" for q in questions)
        )

    def _build_result_schema(self, questions: List[str]) -> Dict[str, Any]:
        """Build JSON Schema for CALL-E structured result extraction."""
        properties = {}
        required_keys = []
        for idx, q in enumerate(questions):
            key = f"question_{idx + 1}"
            properties[key] = {
                "type": "string",
                "description": f"Answer to question: {q}. Return 'Could not verify' if unverified, not answered, or evidence is ambiguous."
            }
            required_keys.append(key)
        return {
            "type": "object",
            "required": required_keys,
            "properties": properties,
            "additionalProperties": False
        }

    def start_call(self, phone_number: str, target_name: str, questions: List[str]) -> Dict[str, Any]:
        print("REAL CALLE start_call() REACHED")
        """
        Step 1: Create the CALL-E call task via calls.create().
        Returns immediately with the real CALL-E call_id.
        Does NOT block waiting for the call to complete.
        """
        task_instruction = self._build_task_instruction(phone_number, target_name, questions)
        result_schema = self._build_result_schema(questions)

        print("CALL-E TASK:", task_instruction)
        print("CALL-E QUESTIONS:", questions)
        print("CALL-E SCHEMA:", result_schema)

        try:
            create_response = self.client.calls.create(
                task=task_instruction,
                result_schema=result_schema,
            )
            print("CALL-E CREATE RESPONSE:", create_response)


        except Exception as e:
           
            print("CALL-E CREATE ERROR:", repr(e))
            print("CALL-E ERROR TYPE:", type(e).__name__)
            print("CALL-E ERROR CODE:", getattr(e, "code", None))
            print("CALL-E ERROR MESSAGE:", getattr(e, "message", None))
            print("CALL-E ERROR STATUS:", getattr(e, "status_code", None))
            print("CALL-E ERROR DETAILS:", getattr(e, "details", None))


            err_msg = str(e)
            error_call_id = f"calle_err_{uuid.uuid4().hex[:10]}"
            self._calls[error_call_id] = {
                "call_id": error_call_id,
                "calle_call_id": None,
                "phone_number": phone_number,
                "target_name": target_name,
                "questions": questions,
                "start_time": time.time(),
                "status": "failed",
                "error_message": err_msg,
                "create_response": None,
                "terminal_response": None,
                "events": None,
            }
            return {
                "call_id": error_call_id,
                "calle_call_id": None,
                "status": "failed",
                "message": f"CALL-E call creation failed: {err_msg}"
            }

        # Extract real CALL-E call task ID from create response
        calle_call_id = create_response.get("id") if isinstance(create_response, dict) else getattr(create_response, "id", None)
        calle_status = create_response.get("status", "created") if isinstance(create_response, dict) else getattr(create_response, "status", "created")

        # Use the CALL-E call ID as our internal ID for direct mapping
        internal_id = calle_call_id or f"calle_{uuid.uuid4().hex[:10]}"

        self._calls[internal_id] = {
            "call_id": internal_id,
            "calle_call_id": calle_call_id,
            "phone_number": phone_number,
            "target_name": target_name,
            "questions": questions,
            "start_time": time.time(),
            "status": calle_status,
            "error_message": None,
            "create_response": create_response,
            "terminal_response": None,
            "events": None,
        }

        return {
            "call_id": internal_id,
            "calle_call_id": calle_call_id,
            "status": "dialing",
            "message": f"CALL-E call task created. Call ID: {calle_call_id}. Dialing {phone_number}..."
        }

    def get_call_status(self, call_id: str) -> Dict[str, Any]:
        """
        Step 2: Poll current call state via calls.get().
        If terminal, retrieve full result via wait_for_result + list_events.
        """
        data = self._calls.get(call_id)

        # If we don't have internal tracking for this call_id, try to fetch directly from CALL-E
        if not data:
            return self._poll_and_map(call_id, call_id, [], "Unknown Target", "+0000000000")

        # If already failed at creation time, return error state
        if data.get("status") == "failed" and data.get("error_message") and not data.get("calle_call_id"):
            return self._build_error_response(data)

        calle_call_id = data.get("calle_call_id") or call_id
        return self._poll_and_map(
            call_id, calle_call_id,
            data["questions"], data["target_name"], data["phone_number"]
        )

    def _poll_and_map(self, internal_id: str, calle_call_id: str,
                      questions: List[str], target_name: str, phone_number: str) -> Dict[str, Any]:
        """Poll CALL-E for current state, retrieve events/transcript if terminal."""
        try:
            call_state = self.client.calls.get(calle_call_id)
        except Exception as e:
            # Transient error – treat as non‑terminal so polling continues.
            return {
                "call_id": internal_id,
                "calle_call_id": calle_call_id,
                "status": "in_progress",
                "message": f"CALL‑E get() transient error: {e}",
                "transcript": [],
                "duration_seconds": 0,
                "hold_seconds": 0,
            }

        status_val = call_state.get("status", "in_progress") if isinstance(call_state, dict) else getattr(call_state, "status", "in_progress")

        # Map CALL-E statuses to our internal status enum
        status_mapping = {
            "created": "dialing",
            "queued": "dialing",
            "in_progress": "speaking",
            "ringing": "dialing",
            "active": "speaking",
        }
        our_status = status_mapping.get(status_val, status_val)

        if status_val in self.TERMINAL_STATUSES:
            return self._build_terminal_response(internal_id, calle_call_id, call_state, questions, target_name, phone_number)

        # Non-terminal: return current polling state
        transcript_turns = self._extract_transcript_turns(call_state)

        return {
            "call_id": internal_id,
            "calle_call_id": calle_call_id,
            "status": our_status,
            "message": f"Call in progress (CALL-E status: {status_val})",
            "transcript": transcript_turns,
            "duration_seconds": call_state.get("duration_seconds", 0) if isinstance(call_state, dict) else getattr(call_state, "duration_seconds", 0),
            "hold_seconds": call_state.get("hold_seconds", 0) if isinstance(call_state, dict) else getattr(call_state, "hold_seconds", 0),
        }

    def _build_terminal_response(self, internal_id: str, calle_call_id: str,
                                  call_state: Any, questions: List[str],
                                  target_name: str, phone_number: str) -> Dict[str, Any]:
        """Build complete response for a call that has reached a terminal state."""
        state = call_state if isinstance(call_state, dict) else {}
        if not isinstance(call_state, dict):
            for attr in ["status", "task_completed", "completion_confidence", "evidence",
                         "structured_result", "duration_seconds", "hold_seconds",
                         "recording_url", "representative", "recipients"]:
                state[attr] = getattr(call_state, attr, None)

        status_val = state.get("status", "completed")
        task_completed = state.get("task_completed", False)
        completion_confidence = state.get("completion_confidence") or {}
        evidence = state.get("evidence") or []
        structured_result = state.get("structured_result")
        duration = state.get("duration_seconds") or 0
        hold_sec = state.get("hold_seconds") or 0
        recording_url = state.get("recording_url")
        representative = state.get("representative")

        # Retrieve events for lifecycle trace
        events = []
        try:
            events_response = self.client.calls.list_events(calle_call_id, limit=50)
            if isinstance(events_response, dict):
                events = events_response.get("events") or events_response.get("data") or []
            elif isinstance(events_response, list):
                events = events_response
        except Exception:
            pass  # Events are supplementary, don't fail the response

        # Extract transcript turns from call state (recipients -> transcript_turns)
        transcript_turns = self._extract_transcript_turns(call_state)

        # If no transcript turns from state, try to build from events
        if not transcript_turns and events:
            transcript_turns = self._extract_transcript_from_events(events)

        # If still no transcript, use evidence as transcript items (never fabricate)
        if not transcript_turns and evidence:
            transcript_turns = [
                {"speaker": "CALL-E Evidence", "text": item, "timestamp": "00:00"}
                for item in evidence
            ]

        # Build answers from structured_result
        answers = self._map_answers(questions, structured_result, task_completed, completion_confidence)

        # Confidence label
        confidence_label = "medium"
        if isinstance(completion_confidence, dict):
            confidence_label = completion_confidence.get("label", "medium")

        # Determine audio/conversation status from evidence
        audio_analysis = self._analyze_call_outcome(status_val, task_completed, evidence, transcript_turns, duration)

        summary_text = (
            f"CALL-E call to {target_name} ({phone_number}). "
            f"Status: {status_val}. Task completed: {task_completed}. "
            f"Confidence: {confidence_label}. "
            f"{audio_analysis}"
        )

        # Update internal tracking
        if internal_id in self._calls:
            self._calls[internal_id]["terminal_response"] = state
            self._calls[internal_id]["events"] = events
            self._calls[internal_id]["status"] = status_val

        return {
            "call_id": internal_id,
            "calle_call_id": calle_call_id,
            "status": status_val if status_val in ("completed",) else "failed",
            "message": summary_text,
            "representative": representative,
            "recording_url": recording_url,
            "duration_seconds": duration,
            "hold_seconds": hold_sec,
            "summary": summary_text,
            "answers": answers,
            "transcript": transcript_turns,
        }

    def _extract_transcript_turns(self, call_state: Any) -> List[Dict[str, Any]]:
        """Extract transcript_turns from CALL-E call state (per-recipient)."""
        state = call_state if isinstance(call_state, dict) else {}
        if not isinstance(call_state, dict):
            state = {"recipients": getattr(call_state, "recipients", None)}

        turns = []
        recipients = state.get("recipients") or []
        for recipient in recipients:
            if isinstance(recipient, dict):
                for turn in (recipient.get("transcript_turns") or []):
                    offset = turn.get("offset_seconds", 0)
                    minutes = int(offset) // 60
                    seconds = int(offset) % 60
                    turns.append({
                        "speaker": turn.get("speaker", "unknown"),
                        "text": turn.get("text", ""),
                        "timestamp": f"{minutes:02d}:{seconds:02d}"
                    })
        return turns

    def _extract_transcript_from_events(self, events: List[Any]) -> List[Dict[str, Any]]:
        """Extract transcript-like information from call lifecycle events. Never fabricate."""
        turns = []
        for event in events:
            ev = event if isinstance(event, dict) else {}
            ev_type = ev.get("type") or ev.get("event_type") or ""
            # Only extract actual speech/transcript events
            if "transcript" in ev_type.lower() or "speech" in ev_type.lower():
                turns.append({
                    "speaker": ev.get("speaker", "unknown"),
                    "text": ev.get("text") or ev.get("content") or str(ev.get("data", "")),
                    "timestamp": ev.get("timestamp", "00:00")
                })
        return turns

    def _map_answers(self, questions: List[str], structured_result: Any,
                     task_completed: bool, completion_confidence: Any) -> List[Dict[str, Any]]:
        """Map CALL-E structured_result to our answer format with unverified fallback."""
        confidence_label = "medium"
        if isinstance(completion_confidence, dict):
            confidence_label = completion_confidence.get("label", "medium")
        if confidence_label not in ("high", "medium", "low"):
            confidence_label = "medium"

        answers = []
        for idx, q in enumerate(questions):
            key = f"question_{idx + 1}"
            ans_val = None
            if isinstance(structured_result, dict):
                ans_val = structured_result.get(key)

            # LOCKED DECISION: If CALL-E does not provide sufficient evidence:
            # answer = "Could not verify", verification = "unverified"
            if (not ans_val
                    or not isinstance(ans_val, str)
                    or ans_val.strip().lower() in ["could not verify", "unknown", "unverified", "none", "null", "n/a"]):
                answers.append({
                    "question": q,
                    "answer": "Could not verify",
                    "confidence": "low",
                    "verification": "unverified"
                })
            else:
                answers.append({
                    "question": q,
                    "answer": ans_val.strip(),
                    "confidence": confidence_label,
                    "verification": "verified" if task_completed else "unverified"
                })

        return answers

    def _analyze_call_outcome(self, status: str, task_completed: bool,
                               evidence: List[str], transcript: List[Dict], duration: int) -> str:
        """Analyze call outcome from CALL-E evidence. Never claim audio worked without evidence."""
        evidence_text = " ".join(evidence).lower() if evidence else ""

        if "declined" in evidence_text or "declined" in status:
            return "Call was declined by recipient before conversation started. No audio exchange occurred."
        if duration == 0 or "zero duration" in evidence_text:
            return "Call had zero duration. No conversation or audio exchange occurred."
        if not transcript and not task_completed:
            return "No transcript captured. Cannot confirm audio/media initialization."
        if transcript and task_completed:
            return f"Call conversation occurred with {len(transcript)} transcript turns."
        if transcript:
            return f"Partial transcript captured ({len(transcript)} turns), but task was not completed."
        return f"Call ended with status '{status}'. Task completed: {task_completed}."

    def finalize_call(self, call_id: str, timeout_seconds: float = 180.0) -> Dict[str, Any]:
        """
        Step 3: Block until call reaches terminal state via wait_for_result().
        Then retrieve events and build final response.
        Use this for explicit synchronous completion (e.g., test scripts).
        """
        data = self._calls.get(call_id)
        if not data:
            return {"status": "failed", "message": f"Call ID {call_id} not found in internal tracking."}

        calle_call_id = data.get("calle_call_id")
        if not calle_call_id:
            return self._build_error_response(data)

        try:
            terminal_state = self.client.calls.wait_for_result(
                calle_call_id,
                timeout_seconds=timeout_seconds,
                interval_seconds=2.0,
            )
            data["terminal_response"] = terminal_state
        except Exception as e:
            data["status"] = "failed"
            data["error_message"] = f"wait_for_result timed out or failed: {e}"
            return self._build_error_response(data)

        return self._build_terminal_response(
            call_id, calle_call_id, terminal_state,
            data["questions"], data["target_name"], data["phone_number"]
        )

    def _build_error_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Build error response for failed calls."""
        err_msg = data.get("error_message", "Unknown error")
        return {
            "call_id": data["call_id"],
            "calle_call_id": data.get("calle_call_id"),
            "status": "failed",
            "message": f"CALL-E call failed: {err_msg}",
            "transcript": [{"speaker": "CALL-E System", "text": f"Error: {err_msg}", "timestamp": "00:00"}],
            "duration_seconds": 0,
            "hold_seconds": 0,
            "answers": [
                {"question": q, "answer": "Could not verify", "confidence": "low", "verification": "unverified"}
                for q in data.get("questions", [])
            ]
        }

    def hangup(self, call_id: str) -> Dict[str, Any]:
        # CALL-E API does not expose a client-side cancel operation (per docs).
        return {"call_id": call_id, "status": "completed", "message": "Hangup requested (CALL-E does not support client-side cancellation)."}

def get_calle_adapter() -> AbstractCalleAdapter:
    mode = (settings.CALLE_MODE or "mock").lower()
    if mode == "real":
        if not settings.CALLE_API_KEY:
            raise ValueError(
                "CALLE_MODE is set to 'real', but CALLE_API_KEY is missing in environment configuration. "
                "Please set CALLE_API_KEY or switch CALLE_MODE=mock."
            )
        return RealCalleAdapter(api_key=settings.CALLE_API_KEY)
    return MockCalleAdapter()

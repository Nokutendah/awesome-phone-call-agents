import sys
import os
import re
import json
import time
from datetime import datetime, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.config import get_settings
from app.db.database import SessionLocal, Base, engine
from app.models.investigation import DBInvestigation, InvestigationStatus

def main():
    print("=== STEP 1: PRE-CALL CONFIGURATION & ENVIRONMENT VALIDATION ===")
    settings = get_settings()

    # 1. Verify CALLE_MODE=real
    print(f"[CHECK 1] CALLE_MODE: {settings.CALLE_MODE}")
    if settings.CALLE_MODE != "real":
        print("[ERROR] Validation Failed: CALLE_MODE is not set to 'real'. Aborting.")
        sys.exit(1)

    # 2. Verify CALLE_API_KEY exists without printing its value
    key_exists = bool(settings.CALLE_API_KEY and len(settings.CALLE_API_KEY) > 10)
    print(f"[CHECK 2] CALLE_API_KEY Present: {key_exists} (Length: {len(settings.CALLE_API_KEY) if settings.CALLE_API_KEY else 0} chars)")
    if not key_exists:
        print("[ERROR] Validation Failed: CALLE_API_KEY is missing or empty. Aborting.")
        sys.exit(1)

    # 3. Verify official calle-ai SDK imports correctly
    try:
        from calle import CalleClient
        print("[CHECK 3] SDK Import ('from calle import CalleClient'): SUCCESS")
    except ImportError as e:
        print(f"[ERROR] Validation Failed: Unable to import CalleClient from calle ({e}). Aborting.")
        sys.exit(1)

    # 4. Verify E.164 phone number format
        
    if len(sys.argv) < 2:
        print("ERROR: Please provide an E.164 phone number.")
        print("Example: python scripts/execute_single_real_call.py +919876543210")
        sys.exit(1)

    raw_phone = sys.argv[1]

    e164_pattern = re.compile(r'^\+[1-9]\d{1,14}$')
    is_e164 = bool(e164_pattern.match(raw_phone))
    print(f"[CHECK 4] Target Phone E.164 Format ('{raw_phone}'): {is_e164}")
    if not is_e164:
        print(f"[ERROR] Validation Failed: Phone '{raw_phone}' is not valid E.164. Aborting.")
        sys.exit(1)

    print("\nAll 4 Pre-Call Validations PASSED cleanly.\n")

        # Target Task and Schema
    task_prompt = f"""
Call {raw_phone}.

You are NOKU, an AI assistant from KPRIET conducting a short conversational test.

Start the conversation naturally. Introduce yourself by saying:

"Hello, this is NOKU from KPRIET calling for a short conversational test."

Then ask:

"How are you doing today?"

Listen carefully to the recipient's response and acknowledge what they say naturally.

Then say:

"I'd like to ask you a few questions. What is one thing you enjoy doing in your free time?"

Listen carefully to their answer.

Based specifically on their answer, ask ONE natural follow-up question about the activity they mentioned.

Listen to their response and acknowledge it naturally.

Then ask:

"Before we finish, is there anything else you'd like to tell me?"

Listen to their response.

Finally, thank them for their time and politely say goodbye.

IMPORTANT CONVERSATION RULES:
- Speak clearly and naturally.
- Do not rush through the questions.
- Wait for the recipient to finish speaking before responding.
- Listen to each answer before asking the next question.
- The follow-up question must relate to the recipient's previous answer.
- Do not repeat a question unless the recipient did not hear or understand it.
- If the recipient gives a short answer, acknowledge it naturally and continue.
- If the recipient asks you a relevant question, respond briefly and naturally before continuing.
- Do not ask for passwords, financial information, medical information, or other sensitive personal information.
- Do not invent information that the recipient did not provide.
- End the call politely after the final question.
"""

    result_schema = {
        "type": "object",
        "required": [
            "how_they_are_doing",
            "favorite_free_time_activity",
            "follow_up_response",
            "anything_else",
            "evidence"
        ],
        "properties": {
            "how_they_are_doing": {
                "type": "string",
                "description": (
                    "Summarize how the recipient said they were doing. "
                    "Return 'Could not verify' if the recipient did not answer "
                    "or the answer was ambiguous."
                )
            },
            "favorite_free_time_activity": {
                "type": "string",
                "description": (
                    "State the free-time activity the recipient said they enjoy. "
                    "Return 'Could not verify' if no clear activity was provided."
                )
            },
            "follow_up_response": {
                "type": "string",
                "description": (
                    "Summarize the recipient's response to the follow-up "
                    "question about their activity. "
                    "Return 'Could not verify' if unavailable or ambiguous."
                )
            },
            "anything_else": {
                "type": "string",
                "description": (
                    "Summarize anything additional the recipient shared "
                    "when asked if there was anything else they wanted to tell us. "
                    "Return 'Could not verify' if they did not provide a meaningful answer."
                )
            },
            "evidence": {
                "type": "string",
                "description": (
                    "Provide concise evidence from the conversation supporting "
                    "the extracted answers. Do not invent information."
                )
            }
        },
        "additionalProperties": False
    }

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    db_item = DBInvestigation(
        mission=task_prompt,
        status=InvestigationStatus.DIALING.value,
        target_name=f"Software Test Target ({raw_phone})",
        phone_number=raw_phone,
        planned_questions=["Can you hear clearly? (yes/no)"],
        answers=[],
        transcript=[]
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    investigation_id = db_item.id

    print("=== STEP 2: LAUNCHING EXPLICIT SINGLE REAL OUTBOUND CALL ===")
    print(f"Investigation ID: {investigation_id}")
    print(f"Target E.164 Phone: {raw_phone}")
    print(f"Task Instruction: {task_prompt}")
    print("Initiating call via CalleClient.calls.create_and_wait ...\n")

    start_time = time.time()
    call_response = None
    call_error = None
    try:
        client = CalleClient(api_key=settings.CALLE_API_KEY)

        # Create the call without waiting for the full call to finish.
        create_response = client.calls.create(
            task=task_prompt,
            result_schema=result_schema
        )

        if isinstance(create_response, dict):
            calle_id = create_response.get("id") or create_response.get("call_id")
        else:
            calle_id = getattr(create_response, "id", None) or getattr(create_response, "call_id", None)

        print(f"CALL-E Call ID: {calle_id}")

        db_item.calle_call_id = calle_id
        db.commit()

       


        if not calle_id:
            raise RuntimeError(f"CALL-E did not return a call ID: {create_response}")

        max_wait_seconds = 600
        poll_interval = 3
        wait_start = time.time()

        while True:
            call_response = client.calls.get(calle_id)

            if isinstance(call_response, dict):
                current_status = call_response.get("status", "unknown")
            else:
                current_status = getattr(call_response, "status", "unknown")

            print(f"CALL-E status: {current_status}")

            if current_status in {"completed", "failed", "canceled", "declined", "error"}:
                break

            if time.time() - wait_start >= max_wait_seconds:
                raise TimeoutError(
                    f"CALL-E call {calle_id} did not finish within {max_wait_seconds} seconds."
                )

            time.sleep(poll_interval)

    except Exception as e:
        call_error = str(e)


    elapsed_duration = int(time.time() - start_time)

    print("=== STEP 3: PROCESSING & PERSISTING CALL-E RESULT TO SQLITE DB ===")

    if call_error:
        print(f"[Call Failure Detected]: {call_error}")
        db_item.status = InvestigationStatus.FAILED.value
        db_item.summary = f"CALL-E call execution failed: {call_error}"
        db_item.answers = [{
            "question": "Can you hear clearly? (yes/no)",
            "answer": "Could not verify",
            "confidence": "low",
            "verification": "unverified"
        }]
        db_item.transcript = [{"speaker": "CALL-E System", "text": f"Error: {call_error}", "timestamp": "00:00"}]
        db.commit()

        print("\n===============================")
        print("      FINAL CALL REPORT        ")
        print("===============================")
        print("CALL-E Call ID: N/A (Call failed during execution)")
        print("Terminal Status: failed")
        print("Task Completed: False")
        print("Completion Confidence: N/A")
        print("Structured Result: None")
        print("Evidence: []")
        print("Transcript Turns: []")
        print(f"Duration: {elapsed_duration} seconds")
        print(f"Error: {call_error}")
        print("===============================\n")
        return

    res_dict = call_response if isinstance(call_response, dict) else {
        "id": getattr(call_response, "id", getattr(call_response, "call_id", "unknown")),
        "status": getattr(call_response, "status", "completed"),
        "task_completed": getattr(call_response, "task_completed", getattr(call_response, "taskCompleted", False)),
        "completion_confidence": getattr(call_response, "completion_confidence", getattr(call_response, "completionConfidence", {})),
        "evidence": getattr(call_response, "evidence", []),
        "structured_result": getattr(call_response, "structured_result", getattr(call_response, "structuredResult", None)),
        "transcript": getattr(call_response, "transcript", []),
        "duration_seconds": getattr(call_response, "duration_seconds", getattr(call_response, "durationSeconds", elapsed_duration)),
        "hold_seconds": getattr(call_response, "hold_seconds", getattr(call_response, "holdSeconds", 0)),
        "recording_url": getattr(call_response, "recording_url", getattr(call_response, "recordingUrl", None)),
        "representative": getattr(call_response, "representative", None),
    }

    calle_id = res_dict.get("id") or res_dict.get("call_id") or "calle_real_task"
    status_val = res_dict.get("status", "completed")
    task_completed = res_dict.get("task_completed", False)
    completion_confidence = res_dict.get("completion_confidence") or {}
    evidence = res_dict.get("evidence") or []
    structured_result = res_dict.get("structured_result") or {}



    # CALL-E stores the real transcript inside:
    # recipients -> attempts -> transcript_turns
    duration = res_dict.get("duration_seconds", elapsed_duration)
    hold_sec = res_dict.get("hold_seconds", 0)


    # CALL-E stores the real conversation transcript inside:
    # recipients -> attempts -> transcript_turns
    transcript = []

    recipients = res_dict.get("recipients") or []

    for recipient in recipients:
        if not isinstance(recipient, dict):
            continue

        attempts = recipient.get("attempts") or []

        for attempt in attempts:
            if not isinstance(attempt, dict):
                continue

            transcript_turns = attempt.get("transcript_turns") or []

            for turn in transcript_turns:
                if not isinstance(turn, dict):
                    continue

                offset = turn.get("offset_seconds")

                if offset is None:
                    timestamp = "00:00"
                else:
                    offset = int(offset)
                    minutes = offset // 60
                    seconds = offset % 60
                    timestamp = f"{minutes:02d}:{seconds:02d}"

                transcript.append({
                    "speaker": turn.get("speaker", "unknown"),
                    "text": turn.get("text", ""),
                    "timestamp": timestamp
                })

    # Only use top-level transcript if CALL-E did not provide
    # the nested recipient/attempt transcript.
    if not transcript:
        transcript = res_dict.get("transcript") or []

    # Last-resort evidence fallback.
    if not transcript and evidence:
        transcript = [
            {
                "speaker": "CALL-E Evidence",
                "text": item,
                "timestamp": "00:00"
            }
            for item in evidence
        ]
   




        # Build answers from the structured CALL-E result.
    answers = []

    confidence_label = "medium"
    if isinstance(completion_confidence, dict):
        confidence_label = completion_confidence.get("label", "medium")

    if confidence_label not in ["high", "medium", "low"]:
        confidence_label = "medium"

    verification_state = "verified" if task_completed else "unverified"

    question_mappings = [
        (
            "How are you doing today?",
            "how_they_are_doing"
        ),
        (
            "What is one thing you enjoy doing in your free time?",
            "favorite_free_time_activity"
        ),
        (
            "What can you tell me about that activity?",
            "follow_up_response"
        ),
        (
            "Is there anything else you'd like to tell me?",
            "anything_else"
        )
    ]

    for question, result_key in question_mappings:
        answer_value = None

        if isinstance(structured_result, dict):
            answer_value = structured_result.get(result_key)

        if (
            not answer_value
            or not isinstance(answer_value, str)
            or answer_value.strip().lower()
            in [
                "could not verify",
                "unknown",
                "unverified",
                "none",
                "null",
                "n/a"
            ]
        ):
            answers.append({
                "question": question,
                "answer": "Could not verify",
                "confidence": "low",
                "verification": "unverified"
            })
        else:
            answers.append({
                "question": question,
                "answer": answer_value.strip(),
                "confidence": confidence_label,
                "verification": verification_state
            })

    # Store the evidence as an additional investigation answer.
    evidence_text = ""

    if isinstance(structured_result, dict):
        evidence_text = structured_result.get("evidence") or ""

    if not evidence_text and evidence:
        evidence_text = " ".join(str(item) for item in evidence)

    if evidence_text:
        answers.append({
            "question": "Evidence from the conversation",
            "answer": evidence_text,
            "confidence": confidence_label,
            "verification": verification_state
        })

    # Persist final investigation state.
    db_item.status = (
        InvestigationStatus.COMPLETED.value
        if status_val == "completed"
        else status_val
    )

    db_item.summary = (
        f"CALL-E call completed to {raw_phone}. "
        f"Task completed: {task_completed}. "
        f"Confidence: {confidence_label}. "
        f"Extracted {len(answers)} result items."
    )

    db_item.answers = answers

    # Persist the real nested CALL-E transcript.
    if transcript:
        db_item.transcript = transcript
    elif evidence:
        db_item.transcript = [
            {
                "speaker": "CALL-E Evidence",
                "text": item,
                "timestamp": "00:00"
            }
            for item in evidence
        ]
    else:
        db_item.transcript = []

    db_item.duration_seconds = duration
    db_item.hold_seconds = hold_sec
    db_item.recording_url = res_dict.get("recording_url")
    db_item.representative = res_dict.get("representative")
    db_item.calle_call_id = calle_id

    db.commit()

    print("\n===============================")
    print("      FINAL REAL CALL REPORT    ")
    print("===============================")
    print(f"CALL-E Call ID: {calle_id}")
    print(f"Terminal Status: {status_val}")
    print(f"Task Completed: {task_completed}")
    print(f"Completion Confidence: {json.dumps(completion_confidence)}")
    print(f"Structured Result: {json.dumps(structured_result, indent=2)}")
    print(f"Evidence: {json.dumps(evidence, indent=2)}")
    print(f"Transcript Turns: {json.dumps(transcript, indent=2)}")
    print(f"Duration: {duration} seconds")
    print(f"Errors: None")
    print("===============================\n")

if __name__ == "__main__":
    main()

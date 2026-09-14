"""
Comprehensive unit tests for CALL-E adapter: RealCalleAdapter async polling flow.

Tests cover:
- Adapter selection (mock vs real mode)
- Missing API key error
- MockCalleAdapter functionality
- Call creation with calls.create() and call ID capture
- Polling via calls.get() for non-terminal and terminal states
- Terminal success with structured_result mapping
- Terminal failure handling
- Timeout handling via wait_for_result
- Transcript retrieval from recipients.transcript_turns
- Structured result retrieval with verified/unverified answers
- Unanswered call (declined, zero duration)
- Unverified answer fallback ("Could not verify")
"""

import pytest
from unittest.mock import MagicMock, patch
from app.config import get_settings
from app.services.calle_adapter import (
    get_calle_adapter,
    MockCalleAdapter,
    RealCalleAdapter,
)


# ──────────────────────────────────────────────────
# 1. Adapter Selection
# ──────────────────────────────────────────────────

def test_adapter_selection_mock(monkeypatch):
    monkeypatch.setattr(get_settings(), "CALLE_MODE", "mock")
    adapter = get_calle_adapter()
    assert isinstance(adapter, MockCalleAdapter)


def test_adapter_selection_real_missing_key(monkeypatch):
    monkeypatch.setattr(get_settings(), "CALLE_MODE", "real")
    monkeypatch.setattr(get_settings(), "CALLE_API_KEY", "")
    with pytest.raises(ValueError, match="CALLE_MODE is set to 'real', but CALLE_API_KEY is missing"):
        get_calle_adapter()


# ──────────────────────────────────────────────────
# 2. MockCalleAdapter Functionality
# ──────────────────────────────────────────────────

def test_mock_adapter_full_lifecycle():
    adapter = MockCalleAdapter()
    start = adapter.start_call("+15551234567", "Test Bakery", ["Do you have cakes?"])
    assert start["status"] == "dialing"
    assert "call_id" in start

    import time
    time.sleep(0.1)
    status = adapter.get_call_status(start["call_id"])
    assert "status" in status


# ──────────────────────────────────────────────────
# 3. Call Creation & Call ID Capture
# ──────────────────────────────────────────────────

def test_real_adapter_call_creation_returns_calle_call_id():
    """calls.create() should return immediately with the CALL-E call_id."""
    mock_client = MagicMock()
    mock_client.calls.create.return_value = {
        "id": "call_ABC123XYZ",
        "status": "created",
    }

    adapter = RealCalleAdapter(api_key="iams_test_key", client=mock_client)
    result = adapter.start_call("+15551234567", "Test Bakery", ["Do you have cakes?"])

    assert result["calle_call_id"] == "call_ABC123XYZ"
    assert result["status"] == "dialing"
    assert result["call_id"] == "call_ABC123XYZ"  # Internal ID matches CALL-E ID

    # Verify calls.create was called (not create_and_wait)
    mock_client.calls.create.assert_called_once()
    mock_client.calls.create_and_wait.assert_not_called()


def test_real_adapter_call_creation_failure():
    """If calls.create() raises, start_call should return error without crashing."""
    mock_client = MagicMock()
    mock_client.calls.create.side_effect = Exception("Authentication failed: invalid API key")

    adapter = RealCalleAdapter(api_key="iams_bad_key", client=mock_client)
    result = adapter.start_call("+15551234567", "Test", ["Q?"])

    assert result["status"] == "failed"
    assert result["calle_call_id"] is None
    assert "Authentication failed" in result["message"]


# ──────────────────────────────────────────────────
# 4. Polling via calls.get() - Non-terminal State
# ──────────────────────────────────────────────────

def test_real_adapter_polling_in_progress():
    """calls.get() returns non-terminal status: adapter maps to our status."""
    mock_client = MagicMock()
    mock_client.calls.create.return_value = {"id": "call_POLL_001", "status": "created"}
    mock_client.calls.get.return_value = {
        "status": "in_progress",
        "duration_seconds": 15,
        "hold_seconds": 0,
        "recipients": [],
    }

    adapter = RealCalleAdapter(api_key="iams_test_key", client=mock_client)
    adapter.start_call("+15551234567", "Test", ["Q1?"])

    status = adapter.get_call_status("call_POLL_001")
    assert status["status"] == "speaking"  # in_progress → speaking
    assert status["calle_call_id"] == "call_POLL_001"
    mock_client.calls.get.assert_called_once_with("call_POLL_001")


# ──────────────────────────────────────────────────
# 5. Terminal Success with Structured Result
# ──────────────────────────────────────────────────

def test_real_adapter_terminal_success_with_structured_result():
    """Terminal completed state with structured_result and transcript_turns."""
    mock_client = MagicMock()
    mock_client.calls.create.return_value = {"id": "call_SUCCESS_001", "status": "created"}
    mock_client.calls.get.return_value = {
        "status": "completed",
        "task_completed": True,
        "completion_confidence": {"score": 0.95, "label": "high"},
        "evidence": ["Sarah confirmed gluten-free cakes are available."],
        "structured_result": {
            "question_1": "Yes, gluten-free cakes are prepared in a sanitized workstation.",
            "question_2": "3 weeks advance notice during peak season."
        },
        "duration_seconds": 45,
        "hold_seconds": 8,
        "recording_url": "https://calle.ai/recordings/call_SUCCESS_001.mp3",
        "representative": "Sarah",
        "recipients": [
            {
                "transcript_turns": [
                    {"offset_seconds": 4, "speaker": "bot", "text": "Hello, this is CallBot."},
                    {"offset_seconds": 8, "speaker": "user", "text": "Hi, how can I help?"},
                    {"offset_seconds": 12, "speaker": "bot", "text": "Do you offer gluten-free cakes?"},
                    {"offset_seconds": 18, "speaker": "user", "text": "Yes, we do!"},
                ]
            }
        ]
    }
    mock_client.calls.list_events.return_value = {"events": []}

    adapter = RealCalleAdapter(api_key="iams_test_key", client=mock_client)
    adapter.start_call("+15551234567", "ABC Bakery", [
        "Do you offer gluten-free wedding cakes?",
        "What is the advance notice requirement?"
    ])

    result = adapter.get_call_status("call_SUCCESS_001")

    assert result["status"] == "completed"
    assert len(result["answers"]) == 2
    assert result["answers"][0]["answer"] == "Yes, gluten-free cakes are prepared in a sanitized workstation."
    assert result["answers"][0]["verification"] == "verified"
    assert result["answers"][0]["confidence"] == "high"
    assert result["answers"][1]["answer"] == "3 weeks advance notice during peak season."
    assert result["answers"][1]["verification"] == "verified"

    # Transcript turns extracted from recipients
    assert len(result["transcript"]) == 4
    assert result["transcript"][0]["speaker"] == "bot"
    assert result["transcript"][0]["timestamp"] == "00:04"
    assert result["transcript"][1]["speaker"] == "user"

    assert result["duration_seconds"] == 45
    assert result["hold_seconds"] == 8
    assert result["representative"] == "Sarah"
    assert result["recording_url"] == "https://calle.ai/recordings/call_SUCCESS_001.mp3"


# ──────────────────────────────────────────────────
# 6. Terminal Failure Handling
# ──────────────────────────────────────────────────

def test_real_adapter_terminal_failure():
    """Terminal failed state: all answers should be 'Could not verify'."""
    mock_client = MagicMock()
    mock_client.calls.create.return_value = {"id": "call_FAIL_001", "status": "created"}
    mock_client.calls.get.return_value = {
        "status": "failed",
        "task_completed": False,
        "completion_confidence": {"score": 0.1, "label": "low"},
        "evidence": ["Call failed: network error connecting to carrier."],
        "structured_result": None,
        "duration_seconds": 0,
        "hold_seconds": 0,
        "recipients": [],
    }
    mock_client.calls.list_events.return_value = {"events": []}

    adapter = RealCalleAdapter(api_key="iams_test_key", client=mock_client)
    adapter.start_call("+15551234567", "Test Shop", ["Are you open?"])

    result = adapter.get_call_status("call_FAIL_001")

    assert result["status"] == "failed"
    assert result["answers"][0]["answer"] == "Could not verify"
    assert result["answers"][0]["verification"] == "unverified"
    assert result["answers"][0]["confidence"] == "low"


# ──────────────────────────────────────────────────
# 7. Timeout Handling (finalize_call with wait_for_result)
# ──────────────────────────────────────────────────

def test_real_adapter_finalize_timeout():
    """wait_for_result() timeout should produce a failed response."""
    mock_client = MagicMock()
    mock_client.calls.create.return_value = {"id": "call_TIMEOUT_001", "status": "created"}
    mock_client.calls.wait_for_result.side_effect = Exception("Timeout: call did not complete within 180s")

    adapter = RealCalleAdapter(api_key="iams_test_key", client=mock_client)
    adapter.start_call("+15551234567", "Test", ["Q?"])

    result = adapter.finalize_call("call_TIMEOUT_001", timeout_seconds=180.0)

    assert result["status"] == "failed"
    assert "Timeout" in result["message"] or "timed out" in result["message"]
    assert result["answers"][0]["answer"] == "Could not verify"


# ──────────────────────────────────────────────────
# 8. Transcript Retrieval from recipients.transcript_turns
# ──────────────────────────────────────────────────

def test_real_adapter_transcript_turns_extraction():
    """Verify transcript_turns are extracted per CALL-E docs format."""
    mock_client = MagicMock()
    mock_client.calls.create.return_value = {"id": "call_TRANS_001", "status": "created"}
    mock_client.calls.get.return_value = {
        "status": "completed",
        "task_completed": True,
        "completion_confidence": {"score": 0.9, "label": "high"},
        "evidence": [],
        "structured_result": {"question_1": "Yes"},
        "duration_seconds": 30,
        "hold_seconds": 0,
        "recipients": [
            {
                "transcript_turns": [
                    {"offset_seconds": 0, "speaker": "bot", "text": "Hello"},
                    {"offset_seconds": 5, "speaker": "user", "text": "Hi there"},
                    {"offset_seconds": 65, "speaker": "bot", "text": "Thank you"},
                ]
            }
        ]
    }
    mock_client.calls.list_events.return_value = {"events": []}

    adapter = RealCalleAdapter(api_key="iams_test_key", client=mock_client)
    adapter.start_call("+15551234567", "Test", ["Q?"])
    result = adapter.get_call_status("call_TRANS_001")

    assert len(result["transcript"]) == 3
    assert result["transcript"][0]["timestamp"] == "00:00"
    assert result["transcript"][1]["timestamp"] == "00:05"
    assert result["transcript"][2]["timestamp"] == "01:05"  # 65 seconds = 1:05
    assert result["transcript"][0]["speaker"] == "bot"
    assert result["transcript"][1]["speaker"] == "user"


# ──────────────────────────────────────────────────
# 9. Unanswered / Declined Call
# ──────────────────────────────────────────────────

def test_real_adapter_unanswered_declined_call():
    """Declined call with zero duration: all answers 'Could not verify'."""
    mock_client = MagicMock()
    mock_client.calls.create.return_value = {"id": "call_DECLINE_001", "status": "created"}
    mock_client.calls.get.return_value = {
        "status": "failed",
        "task_completed": False,
        "completion_confidence": {"score": 0.68, "label": "medium"},
        "evidence": [
            "The call ended immediately with a declined status and zero call duration.",
            "No transcript or speech recognition result was captured."
        ],
        "structured_result": {"question_1": "unknown"},
        "duration_seconds": 0,
        "hold_seconds": 0,
        "recipients": [],
    }
    mock_client.calls.list_events.return_value = {"events": []}

    adapter = RealCalleAdapter(api_key="iams_test_key", client=mock_client)
    adapter.start_call("+916385698827", "Test Target", ["Can you hear clearly?"])

    result = adapter.get_call_status("call_DECLINE_001")

    assert result["status"] == "failed"
    assert result["answers"][0]["answer"] == "Could not verify"
    assert result["answers"][0]["verification"] == "unverified"
    # Verify audio analysis detects zero duration
    assert "zero duration" in result["message"].lower() or "declined" in result["message"].lower()


# ──────────────────────────────────────────────────
# 10. Unverified Answer Fallback
# ──────────────────────────────────────────────────

def test_real_adapter_unverified_answer_mapping():
    """Answers with 'unknown', 'n/a', None should map to 'Could not verify'."""
    mock_client = MagicMock()
    mock_client.calls.create.return_value = {"id": "call_UNVERIFY_001", "status": "created"}
    mock_client.calls.get.return_value = {
        "status": "completed",
        "task_completed": True,
        "completion_confidence": {"score": 0.8, "label": "high"},
        "evidence": ["Partial answer obtained."],
        "structured_result": {
            "question_1": "Yes, we deliver on weekends.",
            "question_2": "unknown",
            "question_3": "Could not verify",
            "question_4": "n/a",
        },
        "duration_seconds": 60,
        "hold_seconds": 0,
        "recipients": [],
    }
    mock_client.calls.list_events.return_value = {"events": []}

    adapter = RealCalleAdapter(api_key="iams_test_key", client=mock_client)
    adapter.start_call("+15551234567", "Delivery Service", [
        "Do you deliver on weekends?",
        "What are your hours?",
        "Do you offer express?",
        "Any discounts?"
    ])

    result = adapter.get_call_status("call_UNVERIFY_001")

    assert result["answers"][0]["answer"] == "Yes, we deliver on weekends."
    assert result["answers"][0]["verification"] == "verified"

    assert result["answers"][1]["answer"] == "Could not verify"
    assert result["answers"][1]["verification"] == "unverified"

    assert result["answers"][2]["answer"] == "Could not verify"
    assert result["answers"][2]["verification"] == "unverified"

    assert result["answers"][3]["answer"] == "Could not verify"
    assert result["answers"][3]["verification"] == "unverified"


# ──────────────────────────────────────────────────
# 11. Call ID Persistence (adapter returns calle_call_id)
# ──────────────────────────────────────────────────

def test_real_adapter_call_id_persistence_in_response():
    """calle_call_id should be present in start_call and get_call_status responses."""
    mock_client = MagicMock()
    mock_client.calls.create.return_value = {"id": "call_PERSIST_001", "status": "created"}
    mock_client.calls.get.return_value = {"status": "in_progress", "recipients": []}

    adapter = RealCalleAdapter(api_key="iams_test_key", client=mock_client)
    start = adapter.start_call("+15551234567", "Test", ["Q?"])

    assert start["calle_call_id"] == "call_PERSIST_001"

    status = adapter.get_call_status("call_PERSIST_001")
    assert status["calle_call_id"] == "call_PERSIST_001"


# ──────────────────────────────────────────────────
# 12. calls.get() Network Error During Polling
# ──────────────────────────────────────────────────

def test_real_adapter_polling_get_error():
    """If calls.get() temporarily fails, keep the call in progress without crashing."""
    mock_client = MagicMock()
    mock_client.calls.create.return_value = {"id": "call_GETERR_001", "status": "created"}
    mock_client.calls.get.side_effect = Exception("Connection timeout")

    adapter = RealCalleAdapter(api_key="iams_test_key", client=mock_client)
    adapter.start_call("+15551234567", "Test", ["Q?"])

    result = adapter.get_call_status("call_GETERR_001")
    assert result["status"] == "in_progress"
    assert "Connection timeout" in result["message"]
    assert "answers" not in result

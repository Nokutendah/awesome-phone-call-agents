"""
Safe test script for CALL-E Integration.
By default, this script verifies SDK installation, client construction, and API key presence
WITHOUT making a real outbound call.

To trigger a live test call, explicitly pass `--live --phone <E164_PHONE>`.
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.config import get_settings

def main():
    parser = argparse.ArgumentParser(description="CallBot Detective CALL-E Test Script")
    parser.add_argument("--live", action="store_true", help="Explicitly enable real outbound test call")
    parser.add_argument("--phone", type=str, default="", help="E.164 phone number for live call")
    args = parser.parse_args()

    settings = get_settings()
    print("=== CALL-E Integration Status ===")
    print(f"CALLE_MODE: {settings.CALLE_MODE}")
    print(f"API Key Present: {'Yes (Length ' + str(len(settings.CALLE_API_KEY)) + ')' if settings.CALLE_API_KEY else 'No'}")

    try:
        from calle import CalleClient
        print("SDK Package 'calle-ai': Installed (import successful)")
    except ImportError as e:
        print(f"SDK Package 'calle-ai': NOT INSTALLED ({e})")
        sys.exit(1)

    if not settings.CALLE_API_KEY:
        print("\n[Warning] CALLE_API_KEY is not set. Real mode will fail.")
        if not args.live:
            print("Safe test completed successfully (SDK verified, no API key present).")
            return

    try:
        client = CalleClient(api_key=settings.CALLE_API_KEY or "iams_test_dummy_key")
        print("CalleClient Instance Created: Success")
    except Exception as e:
        print(f"CalleClient Initialization Failed: {e}")
        sys.exit(1)

    if not args.live:
        print("\n[SAFE MODE] Real outbound call was NOT executed.")
        print("To run a live test call, execute:")
        print("  python scripts/test_calle.py --live --phone +15550192834")
        return

    if not args.phone:
        print("\n[Error] --live flag requires a valid E.164 phone number via --phone <NUMBER>")
        sys.exit(1)

    print(f"\n[LIVE MODE ACTIVATED] Launching real call to {args.phone}...")
    try:
        res = client.calls.create_and_wait(
            task=f"Call {args.phone} and ask whether they can hear clearly.",
            result_schema={
                "type": "object",
                "required": ["can_hear_clearly"],
                "properties": {
                    "can_hear_clearly": {"type": "string", "enum": ["yes", "no", "unknown"]}
                }
            }
        )
        print("Live Call Response:", res)
    except Exception as e:
        print("Live Call Failed:", e)

if __name__ == "__main__":
    main()

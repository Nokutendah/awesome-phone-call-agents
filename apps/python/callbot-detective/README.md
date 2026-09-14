# CallBot Detective

CallBot Detective is a customer-facing application that turns a natural-language investigation mission into a real phone call, captures conversation evidence, and returns structured intelligence.

## CALL-E integration

The application uses the CALL-E API/SDK to place outbound calls. The backend plans questions from the investigation mission, starts a CALL-E call, polls its status, and maps the completed call into a structured investigation report.

## Setup

1. Create a Python environment and install the backend dependencies.
2. Configure the required environment variables in a local `.env` file.
3. Set `CALLE_MODE=real` and provide `CALLE_API_URL` and `CALLE_API_KEY`.
4. Never commit credentials, `.env` files, call records, or personal data.

Example configuration:

```env
CALLE_MODE=real
CALLE_API_URL=https://api.heycall-e.com/v1
CALLE_API_KEY=YOUR_CALL_E_API_KEY
```

## Usage and side effects

The application supports real outbound phone calls. Starting an investigation in real mode has an external side effect: CALL-E may place a call to the configured target. Only start calls when the operator has reviewed the target, mission, and questions and has authorization to contact the recipient.

For development and testing, use the application's non-real/test mode where available. Do not use real phone numbers or credentials in examples or automated tests.

## Safety and privacy

- Keep API credentials in environment variables or a secret manager.
- Use only phone numbers you are authorized to contact.
- Review call targets and questions before initiating real calls.
- Treat transcripts and structured results as potentially sensitive data.
- Do not use the prototype for emergency decisions without appropriate human verification.
- If evidence is unavailable, the application should represent it as unverified rather than inventing an answer.

## Architecture

The integration follows this flow:

`Mission → Question Planning → CALL-E Call → IVR / Conversation → Evidence Capture → Structured Result → Investigation Report`

The full CallBot Detective project, including its web frontend and backend, is maintained separately from this contribution package.

# CallBot Detective

> AI Phone Investigator that calls businesses and customer-service lines, asks targeted questions, navigates phone trees (IVR), and turns phone conversations into structured answers.

Built for **CALL-E: Your Code Is Calling** Hackathon.

## Purpose & Features
- **Natural Language Mission Input**: Users type a mission (e.g. "Call ABC Bakery and check if they make gluten-free wedding cakes").
- **AI Mission Planning**: Powered by Gemini structured output, CallBot Detective extracts target name, phone number, and specific questions.
- **Human-in-the-Loop Confirmation**: Pre-call review screen displaying target details and planned questions before dialing.
- **Official CALL-E Telephony Engine Integration**: Support for both simulated (`CALLE_MODE=mock`) and real outbound telephony calls (`CALLE_MODE=real`) via the official `calle-ai` Python SDK.
- **Structured Post-Call Reports**: Includes executive summary, question-by-question verification states (`verified`, `unverified`, `not_answered`, `contradicted`), representative name, duration, transcript, and audio recording.
- **Local Persistence**: Powered by SQLite for zero-config local history.

## Architecture

```
callbot-detective/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI Application Entry
│   │   ├── config.py          # Environment Settings (CALLE_MODE, CALLE_API_KEY)
│   │   ├── db/                # SQLite Database Engine
│   │   ├── models/            # SQLAlchemy & Pydantic Data Models
│   │   ├── routes/            # REST API Endpoint Routers
│   │   └── services/          # Planner, CALL-E Adapter, & Analyzer Services
│   ├── scripts/
│   │   └── test_calle.py      # Safe CALL-E Integration & Test Script
│   ├── tests/                 # Pytest Test Suite
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/               # Next.js App Router Pages & Layout
│   │   ├── components/        # Mission, Live Call, Report, & History UI
│   │   ├── lib/               # API Fetch Helpers
│   │   └── types/             # Shared TypeScript Type Interfaces
│   └── package.json
└── docs/                      # Hackathon Build Notes & Specs
```

---

## CALL-E Integration & Configuration

### Environment Variables
Configure the following in `backend/.env`:

```env
# Telephony Engine Mode: "mock" (default, safe for local testing) or "real" (makes outbound calls via CALL-E)
CALLE_MODE=mock

# CALL-E Developer API Key (Required when CALLE_MODE=real)
CALLE_API_KEY="api here"

# Database & Gemini AI Settings
DATABASE_URL=sqlite:///./callbot.db
GEMINI_API_KEY=your_gemini_api_key_here
```

> [!WARNING]
> **IMPORTANT SECURITY & SAFETY NOTICE**:
> - `CALLE_API_KEY` is strictly handled on the backend server. It is NEVER exposed to the browser or frontend client.
> - Setting `CALLE_MODE=real` enables live outbound telephony calls. Live calls consume CALL-E credits and dial actual target phone numbers.
> - CallBot Detective will **never** automatically initiate a real outbound call without explicit user confirmation.

---

### How to Run Mock Mode (Default)
In mock mode, the application simulates realistic phone tree navigation (`dialing` $\rightarrow$ `ivr` $\rightarrow$ `holding` $\rightarrow$ `speaking` $\rightarrow$ `analyzing` $\rightarrow$ `completed`) without placing real phone calls.

```bash
# Set in backend/.env:
CALLE_MODE=mock
```

---

### How to Enable Real Mode
To connect to the live CALL-E Telephony API:

1. Obtain your API Key from the [CALL-E Dashboard](https://dashboard.heycall-e.com/account/api-keys).
2. Set in `backend/.env`:
   ```env
   CALLE_MODE=real
   CALLE_API_KEY=your_live_calle_api_key
   ```
3. Restart the backend server (`uvicorn app.main:app --reload --port 8000`).

If `CALLE_MODE=real` is configured without a valid `CALLE_API_KEY`, the application will return a clear configuration error instead of silently falling back to simulation.

---

### How to Perform Your First Authorized Test Call

To verify your CALL-E API key and SDK setup safely **WITHOUT** placing a real call:

```powershell
cd backend
.\venv\Scripts\python.exe scripts/test_calle.py
```

When you are ready to make your **FIRST real authorized test call** to a number you own or are authorized to call, run:

```powershell
cd backend
.\venv\Scripts\python.exe scripts/test_calle.py --live --phone +15550192834
```

> Replace `+15550192834` with your E.164 formatted target phone number.

---

## Local Setup & Development

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
pnpm install
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Testing & Verification Commands

- **Backend Pytest Test Suite**:
  ```bash
  cd backend
  python -m pytest
  ```
- **Frontend Type & Build Checks**:
  ```bash
  cd frontend
  npx tsc --noEmit
  pnpm build
  ```

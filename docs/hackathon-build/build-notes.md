# Hackathon Build Notes - CallBot Detective

## Project Purpose
CallBot Detective is an autonomous AI phone investigator built for the **CALL-E: Your Code Is Calling** hackathon. It receives natural-language mission prompts, plans targeted questions, confirms call details with the user, dials via an isolated CALL-E adapter, navigates IVR phone trees, captures live call transcripts, and converts phone conversations into structured, verified Q&A reports.

## Build Log

### Milestone 1: Project Bootstrap (Completed)
- **Files Created**:
  - `backend/app/main.py`: FastAPI server setup with CORS, router registration, SQLite DB initialization.
  - `backend/app/config.py`: Environment configuration via Pydantic BaseSettings.
  - `backend/app/db/database.py`: SQLAlchemy SQLite engine & session management.
  - `backend/app/routes/health.py`: Health check endpoint (`/api/health`).
  - `backend/requirements.txt`: Backend dependencies.
  - `frontend/src/app/layout.tsx`, `page.tsx`, `globals.css`: Next.js 14 layout & styling tokens.
  - `frontend/package.json`, `tsconfig.json`, `tailwind.config.js`, `next.config.js`: Frontend scaffolding & API proxy rewrite.
  - `.env.example`: Config template.
  - `README.md` & `docs/hackathon-build/build-notes.md`: Documentation.
- **Verification**: `python -m pytest` executed and passed (`test_health.py`).

### Milestone 2: Investigation Data Model & Storage (Completed)
- **Files Created**:
  - `backend/app/models/investigation.py`: SQLAlchemy `DBInvestigation` table & Pydantic request/response models.
  - `backend/app/routes/investigations.py`: REST endpoints (`POST /api/investigations`, `POST /api/investigations/{id}/start`, `GET /api/investigations/{id}`, `GET /api/investigations`).
  - `frontend/src/types/investigation.ts`: Shared TypeScript interfaces.
  - `backend/tests/test_investigations.py`: Pytest suite for DB CRUD operations.
- **Verification**: `pytest` passed 2/2 tests cleanly.

### Milestone 3: Mission Planner - Gemini AI (Completed)
- **Files Created**:
  - `backend/app/services/planner.py`: Gemini AI mission planner (`plan_mission`). Extracts target business name, phone number, planned questions, and confidence rating.
  - Fallback heuristic planner for keyless or offline test environments.
- **Rules Enforced**: If phone number or target business cannot be confidently identified, status is set to `needs_user_input`.

### Milestone 4: Mission UI & Pre-Call Confirmation (Completed)
- **Files Created**:
  - `frontend/src/components/ConfirmationModal.tsx`: Pre-call review modal displaying target, phone number (editable), and planned questions.
  - `frontend/src/app/page.tsx`: Mission input screen with quick-demo presets.

### Milestone 5: CALL-E Telephony Adapter Engine (Completed)
- **Files Created**:
  - `backend/app/services/calle_adapter.py`: Isolated telephony engine service interface (`AbstractCalleAdapter`), `MockCalleAdapter` with realistic state machine (`dialing` -> `ivr` -> `holding` -> `speaking` -> `analyzing` -> `completed`), and `RealCalleAdapter` stub.
- **Design Decision**: CALL-E calls are strictly isolated behind the adapter interface.

### Milestone 6: Live Investigation UI (Completed)
- **Files Created**:
  - `frontend/src/components/LiveCallView.tsx`: Real-time call dashboard featuring status badges, active audio equalizer animation, streaming transcript view, duration timer, and hold time tracking.

### Milestone 7: Conversation Analysis - Gemini AI (Completed)
- **Files Created**:
  - `backend/app/services/analyzer.py`: Gemini AI transcript analyzer (`analyze_transcript`).
- **Product Policy Enforced**: Unverified questions explicitly output `"Could not verify"` with `unverified` status. Zero hallucinated answers.

### Milestone 8: Case Report UI (Completed)
- **Files Created**:
  - `frontend/src/components/CaseReportView.tsx`: Structured executive summary, question-by-question answer cards with color-coded verification badges (`Verified` = Green, `Unverified` = Amber), representative name, call duration, hold time, audio player, and transcript viewer.

### Milestone 9: Investigation History (Completed)
- **Files Created**:
  - `frontend/src/components/InvestigationHistory.tsx`: Filterable history list backed by SQLite database.
  - `frontend/src/app/history/page.tsx` & `frontend/src/app/investigation/[id]/page.tsx`: Deep-linkable investigation report pages.

### Milestone 10 & 11: Hardening & Verification (Completed)
- Clean test execution (`python -m pytest` -> 2 passed).
- Frontend package setup with pnpm (`pnpm install`).
- Verified proxy rewrite configuration to FastAPI backend port 8000.

### Real CALL-E Integration Milestone (Completed)
- **Actions**:
  - Installed official `calle-ai` Python SDK (`v0.7.0`).
  - Implemented `RealCalleAdapter` in `backend/app/services/calle_adapter.py` using `CalleClient`.
  - Added environment configuration `CALLE_MODE` (`mock` or `real`) and `CALLE_API_KEY` in `backend/app/config.py`.
  - Enforced strict security: API key is isolated on backend and never exposed to the frontend/browser.
  - Implemented task instruction & JSON result schema generation matching target business, E.164 phone, mission, and planned questions.
  - Implemented unverified fallback rule: If evidence is missing, output `verification = "unverified"` and `answer = "Could not verify"`.
  - Added safe test script `backend/scripts/test_calle.py` to test SDK import and client setup without making a real call.
  - Added unit test suite `backend/tests/test_calle_adapter.py` (6 tests total, 100% passing).
- **Verification**: `python -m pytest` passed 6/6 tests.


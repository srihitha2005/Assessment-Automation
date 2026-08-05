# Assessment Automation

End-to-end pipeline that turns a curriculum planner's learning outcomes into a live, portal-published assessment — with generated questions, image-embedding DOCX/PDF exports, lossless doc parsing, immutable version snapshots, hard-locked student submissions, and dynamic planner-change propagation.

Built for the **Technical Assessment: End-to-End Assessment Automation** brief. Satisfies Option A (functional Docker container) and inlines Option B (system blueprint) as `docs/blueprint.md`.

---

## Clone and run (one command)

Prereq: **Docker Desktop** running.

```bash
git clone https://github.com/srihitha2005/Assessment-Automation.git
cd Assessment-Automation
docker compose up --build
```

First build pulls Postgres + Python + Node + nginx images (~3–5 min). After that:

- **Frontend UI:** http://localhost:5173
- **Backend Swagger:** http://localhost:8000/docs

The backend auto-creates the schema and seeds one demo assessment for the *Digestive System* planner on first boot, so the Dashboard and Assessments list have real content immediately.

**Optional — for real LLM-generated questions:** install [Ollama](https://ollama.com/download) on the host and run `ollama pull qwen2.5:3b && ollama serve`. The backend container reaches it via `host.docker.internal:11434`. Without Ollama, the pipeline still works using deterministic heuristics.

---

## Quickstart without Docker (60 seconds)

```bash
# 1. backend
cd backend
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

Backend starts on `http://localhost:8000` using SQLite (`backend/backend.db`). The first boot generates one demo assessment for the *Digestive System* planner so the UI has content.

```bash
# 2. frontend (in another shell)
cd frontend
npm install
npm run dev
```

Frontend opens on `http://localhost:5173` and proxies `/api` to the backend.

Optional: start Ollama and pull `qwen2.5:3b` so LLM classification/generation kick in — the pipeline runs without it too, using deterministic heuristics.

```bash
ollama serve
ollama pull qwen2.5:3b
```

---

## What it does

```
┌──────────────────────────────┐        ┌──────────────────────────────┐
│  React 19 + Vite + RQ + MUI  │──HTTP──▶  FastAPI + SQLAlchemy        │
│  Dashboard · Curriculum ·    │        │  Wired controllers ▶ services│
│  Planners · Assessments ·    │        │  ▶ repositories ▶ SQLite/PG  │
│  Editor · Publish · Versions │        │                              │
│  · Propagation · Question    │        │  Ollama (qwen2.5:3b)         │
│  Bank                        │        │  reportlab · python-docx     │
└──────────────────────────────┘        └──────────────────────────────┘
```

**Phase 1 — Intelligent generation.**  Planner outcomes + grade drive a blueprint (question count, difficulty ratio, Bloom distribution, question-type mix). The engine seeds from the on-disk question bank, LLM-classifies each candidate, scores against the blueprint, and only asks Ollama for the gaps. If Ollama is unavailable, deterministic heuristics still produce a valid assessment.

**Phase 1 — Compilation.**  DOCX export embeds real images and appends a hidden JSON footer so parsing round-trips losslessly. PDF export (ReportLab) mirrors the layout.

**Phase 2 — Doc → portal.**  Parsing prefers the JSON footer; falls back to a regex reader for teacher-edited docs. Publish signs the payload with SHA-256, POSTs to `PORTAL_PUBLISH_URL` with a Bearer token when configured, retries with jittered backoff — or writes a signed JSON artifact to `generated_documents/portal_<id>.json` for the demo.

**Stretch — Teacher dashboard.**  `/api/dashboard/summary` aggregates assessments, submissions and propagation events. The publish action synchronises it inline.

**Stretch — Immutability & version control.**  Every mutation snapshots the assessment (`AssessmentVersion`). Student submissions freeze the assessment view into `Submission.locked_snapshot` — edits to the live assessment never touch that row.

**Stretch — Dynamic outcome propagation.**  `POST /api/planners/{id}/outcomes` diffs old vs new outcomes, marks all Published assessments tied to the planner as `Outdated`, and records a `PropagationEvent` that the UI shows.

---

## Demo script

1. `docker compose up --build` — wait for the *backend* health check.
2. Open <http://localhost:5173>. Dashboard shows one seeded assessment.
3. **Planners → Digestive System Planner → Generate assessment**. Redirects to the editor.
4. Inline-edit any question, upload an image, regenerate the answer.
5. **Download DOCX** and **PDF** — images embedded.
6. **Parse DOCX** — result matches editor state (source: `metadata`).
7. **Publish** → confirm on the preview page → status flips to *Published* and digest is displayed.
8. **Record submission** on the editor page (exact-match auto-scored). Edit a question afterwards; the submission's locked snapshot still shows the old text.
9. **Version history** → rollback to v1. `bloomsLevel` and `learningOutcomes` preserved (verifies rollback fix).
10. Back on **Planner** → *Edit outcomes (simulate)* → add a new outcome. **Propagation** page shows the diff; the assessment status flips to *Outdated*.

Run the automated smoke test instead: `python scripts/smoke_test.py`.

---

## Environment

Backend (see `backend/.env.example`):

| Var | Default | Purpose |
|-----|---------|---------|
| `DATABASE_URL` | `sqlite:///backend/backend.db` | Set to `postgresql+psycopg://…` for Postgres |
| `OLLAMA_URL` | `http://localhost:11434` | Local Ollama instance |
| `OLLAMA_MODEL` | `qwen2.5:3b` | Which model to use |
| `OLLAMA_CLASSIFY_BATCH_SIZE` | `8` | Chunk size for batched classification |
| `PORTAL_PUBLISH_URL` | unset | Enables real portal publish |
| `PORTAL_API_KEY` | unset | Sent as `Authorization: Bearer …` |
| `BOOTSTRAP_DEMO_DATA` | `true` | Seed one assessment on first boot |
| `ENABLE_PDF_EXPORT` | `true` | Toggle ReportLab PDF path |
| `GOOGLE_SPREADSHEET_ID`, `GOOGLE_SERVICE_ACCOUNT_FILE` | local Assessment_automation defaults | Read curriculum/planners from Sheets |
| `GOOGLE_CURRICULUM_SHEET`, `GOOGLE_PLANNER_SHEET` | `Curriculum`, `Planner_details` | Source tab names |

Frontend: `VITE_API_BASE_URL` (default `/api` via Vite proxy).

---

## Layout

```
backend/                     FastAPI service
    controller/              Thin HTTP layer, wired to services
    service/                 Business logic (assessment, publish, doc, ollama, submission, propagation, dashboard, curriculum, image, question_bank)
    repository/              CRUD queries only
    entity/                  SQLAlchemy models (dialect-neutral GUID)
    data/                    Google Sheets + question-bank index
    prompts/                 LLM prompt templates (loaded at import)
frontend/                    React 19 + Vite + React Query
    src/components/ui/       Design-token primitives
    src/components/assessment/, question/  Feature components
    src/pages/               One file per route
    src/hooks/               React Query mutations/queries
    src/lib/                 axios instance, query client, api, format, constants
Question Bank/               30 chapter JSONs + images
scripts/smoke_test.py        Live HTTP end-to-end check
docs/blueprint.md            System blueprint (Option B content)
docker-compose.yml           Postgres + backend + frontend
```

---

## Design notes

- **Portable UUID**: `database.GUID` decays to `CHAR(36)` on SQLite, `UUID` on Postgres — same schema, either backend.
- **Snapshots are the source of truth for rollback**: every mutation writes a `snapshot` dict identical to the API response shape. Rollback rebuilds every question through the canonical `_row_from_dict` helper, so nothing is lost.
- **Chunked classification** (`OLLAMA_CLASSIFY_BATCH_SIZE=8`): keeps qwen2.5:3b honest about `index` fields. Missing indices fall back to deterministic heuristics per question, not per batch.
- **Generation never raises**: if a slot fails all retries, a clearly-marked placeholder is inserted and the question is flagged `needsReview=True` in the UI.
- **Publish**: signed digest recorded on the assessment; retries only on 5xx.
- **Doc round-trip**: hidden JSON footer preserves `questionType`, `bloomLevel`, `learningOutcomes` that a visible parser would lose.

See `docs/blueprint.md` for the full architecture, API schemas, prompt templates, and error strategy.

### Google Sheets planner setup

The local defaults use `backend/google_credentials.json` and the configured
`Assessment_automation` workbook. Create a `Planner_details` tab with the required
headings `Planner_name` and `Planer_link` (the supplied spelling is supported).
Optional `Planner_ID`, `Curriculum_ID`, `Learning_Outcomes`, `Grade`,
`Course_Name`, `Unit_Name`, and `Chapter_Name` columns are also understood. When
only a name and Google Docs link are supplied, the app derives a stable planner ID,
parses the linked document on demand, and matches its chapter to the `Curriculum`
tab. Share each document with the service-account email from the credential file,
then use **View parsed planner** before generating an assessment.

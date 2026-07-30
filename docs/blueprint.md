# System Blueprint

This document satisfies the *Option B (System Blueprint Worksheet)* deliverable from the assessment brief. It complements the running codebase (Option A) with the design rationale behind it — architecture, API schemas, OCR/doc-parsing flow, LLM prompt templates, and error-handling strategy.

---

## 1. Architecture

```
┌──────────────────────────────┐        ┌──────────────────────────────┐
│  React 19 + Vite             │──HTTP──▶  FastAPI + SQLAlchemy        │
│  React Query, react-hot-toast│        │                              │
│  Pages: Dashboard,           │        │  Controller (thin)           │
│  Curriculum, Planners,       │        │      │                       │
│  Assessments, Editor,        │        │      ▼                       │
│  Publish, Versions,          │        │  Service (business rules)    │
│  Propagation, QB Browser     │        │      │                       │
└──────────────────────────────┘        │      ▼                       │
                                        │  Repository (queries)        │
                                        │      │                       │
                                        │      ▼                       │
                                        │  Entity (SQLAlchemy, GUID)   │
                                        │      │                       │
                                        │      ▼                       │
                                        │  SQLite (dev) / Postgres     │
                                        │                              │
                                        │  Adjacent services:          │
                                        │  • OllamaService (qwen2.5)   │
                                        │  • DocumentService (docx/pdf)│
                                        │  • PublishService (portal)   │
                                        │  • QuestionBankService (json)│
                                        │  • SubmissionService (lock)  │
                                        │  • PropagationService (diff) │
                                        │  • DashboardService (agg)    │
                                        │  • CurriculumService (sheets)│
                                        │  • ImageService (uploads)    │
                                        └──────────────────────────────┘
```

The **service layer is the API contract**. Controllers only marshal HTTP; every business rule lives in `service/*`. This lets us swap FastAPI for a CLI or a queue consumer without touching pipeline logic.

---

## 2. Data model

| Table | Purpose |
|-------|---------|
| `assessment` | one row per generated assessment; carries `learning_outcomes`, `validation_report`, `publish_target`, `publish_digest`, `published_on` |
| `assessment_question` | one row per question; `needs_review` flag; `learning_outcomes` array |
| `assessment_version` | append-only snapshots (JSON) — the source of truth for rollback |
| `submission` | student submissions; `locked_snapshot` freezes the assessment at submission time |
| `propagation_event` | planner-outcome diff (previous/new/added/removed + affected assessment ids) |
| `question_image` | uploaded question images metadata (files under `uploaded_images/`) |

Every UUID column uses `database.GUID`: a `TypeDecorator` that stores as native `UUID` on Postgres and `CHAR(36)` on SQLite. Same schema, both dialects.

---

## 3. Pipeline flow

### 3.1 Generate

1. Load planner + curriculum from Google Sheets fallback (`GoogleSheetsDataSource`).
2. Build a **blueprint** deterministically: question count = `min(20, max(8, |outcomes| * 3))`; difficulty ratio by grade band; Bloom distribution by grade band; question-type distribution fixed to `QUESTION_TYPE_RATIOS`.
3. Load candidate questions from the on-disk question bank (`QuestionBankService.load_questions`), skipping any text used before for the same planner (queried across live rows AND historical snapshots — `_used_question_texts`).
4. Batch-classify candidates via `OllamaService.classify_many` in chunks of 8. Missing indices in the LLM response fall through to `_heuristic_classification`.
5. `_select` greedy-scores candidates against each blueprint slot; slots that don't hit ≥6 (learning-outcome match required) become **gaps**.
6. `_generate_missing` asks the LLM per gap up to `MAX_GENERATION_RETRIES`; anything still unfilled becomes a clearly-marked placeholder with `needsReview=True` — pipeline never raises.
7. Normalise marks to hit the blueprint total, run `_validation_report` (advisory), persist the assessment + questions, write the initial `AssessmentVersion` snapshot.

### 3.2 Compile (DOCX + PDF)

- `DocumentService.create_docx` (python-docx): headings, options as bullets, image via `add_picture` (falls back to a `[image: path]` line if the file is missing), an italicised metadata line (type / difficulty / Bloom / outcomes), and finally an **invisible `[JSON_METADATA]` marker plus a 1-pt JSON blob** of the full schema.
- `DocumentService.create_pdf` (reportlab): identical layout, images sized to 3.5" × 2.2".

### 3.3 Parse

`DocumentService.parse_docx` searches for the JSON footer first. If found, returns the exact schema — lossless round-trip. Otherwise regex-parses visible content (fallback for teacher-edited docs). The response includes `source: "metadata"|"regex"` so callers can react.

### 3.4 Publish

`PublishService.publish`:
1. Serialise the payload with sorted keys → canonical bytes.
2. SHA-256 the bytes → `X-Content-Digest: sha256=<hex>` header.
3. If `PORTAL_PUBLISH_URL`: POST with 30 s timeout, up to 3 retries with jittered exponential backoff. 4xx aborts immediately; 5xx retries.
4. If no portal URL: write a signed JSON wrapper to `generated_documents/portal_<id>.json` — the demo has a real artifact to inspect.
5. Persist `publish_target`, `publish_digest`, `published_on` on the assessment inside the same transaction; snapshot the mutation as `ACTION_PUBLISHED`.

### 3.5 Rollback (Immutability & Version Control)

Every mutation writes an `AssessmentVersion` snapshot with the API-shape payload before the change happens. `AssessmentService.rollback`:

1. Fetch the target snapshot.
2. Write a new snapshot with `ACTION_ROLLED_BACK` first (so rollback is itself reversible).
3. Restore scalar fields; wipe current questions; call `_replace_questions` with the snapshot's `questions` array. Every question flows through `_row_from_dict` which handles both `bloomLevel` and `bloomsLevel` keys and defaults marks consistently — this is what fixes the previous rollback bug where `bloomsLevel` mapped to the wrong column.

**Submissions never mutate.** Editing a live assessment increments `assessment.version` but touches nothing on `submission.locked_snapshot`. A submission recorded against v1 continues to display the v1 questions even after v2 exists.

### 3.6 Dynamic outcome propagation

`PropagationService.update_planner_outcomes(planner_id, new_outcomes, user)`:

1. Fetch current planner outcomes.
2. Compute added / removed diff.
3. Overlay the new outcomes in-memory (`GoogleSheetsDataSource.override_planner_outcomes`) so subsequent generates see them.
4. Mark every Published assessment for the planner as `Outdated` — teachers keep control of when to regenerate.
5. Write a `PropagationEvent` with the full diff + affected ids.
6. UI: `/propagation` shows the feed; the teacher dashboard reflects the count.

### 3.7 Teacher dashboard sync

`DashboardService.summary` aggregates totals, per-status counts, average marks, five most-recent assessments, and five most-recent submissions. Publish invalidates the dashboard cache via React Query so the panel updates atomically.

---

## 4. Prompt templates

Every prompt is a file in `backend/prompts/`, loaded once at import and format-string-templated per call. Placeholders match Python `str.format`.

### 4.1 `classify_prompt.txt`

```
You are an expert curriculum designer. Classify each numbered {grade} question against the supplied learning outcomes.

Learning outcomes: {learning_outcomes_json}
Allowed question types: {question_types_json}
Allowed difficulty levels: Easy, Medium, Hard
Allowed Bloom levels: Remember, Understand, Apply, Analyze, Evaluate, Create

For each question, return a classification with:
- index (int, 0-based)
- difficulty
- bloomLevel
- questionType
- learningOutcomes (subset of the supplied list)
- marks (1–5)

Return JSON only in the exact shape:
{{"classifications":[{{"index":0,"difficulty":"...",...}}]}}

Questions: {questions_json}
```

Batched in chunks of `OLLAMA_CLASSIFY_BATCH_SIZE=8` to prevent qwen2.5:3b from dropping indices on long prompts.

### 4.2 `generate_prompt.txt`

Instructs the model to generate ONE original question meeting difficulty / Bloom / type / marks / outcome constraints, adapted to grade-appropriate vocabulary. Includes explicit rules for MCQ / True-False / Fill-in-the-Blank shapes so the JSON is directly usable.

### 4.3 `answer_prompt.txt`

Rewrites a model answer for an existing question, given its outcomes and grade. Returns `{"answer": "..."}`.

---

## 5. Error strategy

- **Global exception handler** in `main.py` maps `LookupError → 404`, `ValueError → 400`, `RuntimeError → 502`, everything else → 500.
- **Never raise from generate**: if the LLM fails, we insert a `needsReview` placeholder and surface it in the UI (badge + toolbar warning) — teachers see exactly what needs their attention.
- **Publish retries** only on 5xx; 4xx surfaces immediately so the teacher can fix the payload.
- **Snapshot BEFORE mutation**: rollback stays correct even if the mutation itself is interrupted.
- **Frontend** wraps every mutation in React Query with `onError → toast.error(...)`; every query has `retry: 1` so a transient blip is invisible.

---

## 6. Non-goals & known limitations

- **No student auth**: submissions accept any `studentId` — this is a pipeline demo, not an LMS.
- **Portal integration is generic**: any HTTP endpoint that accepts the payload works. Real LMS bindings (Canvas, Moodle, etc.) would live in per-provider adapters that call `PublishService.publish`.
- **Ollama** is a local dependency of the *ideal* path. The pipeline degrades gracefully to heuristics, but qwen2.5:3b makes generated questions substantially better.
- **Google Sheets fallback** covers 10 planners and 30 chapters — enough for a demo. A real deployment would wire a real spreadsheet.

---

## 7. Testing

- `scripts/smoke_test.py` — exercises every controller against a live backend and prints a per-step report. Used both in CI and as the demo script.
- **Manual UI walkthrough** — 10-step demo in the README, verifiable end-to-end.

---

## 8. What was fixed vs. the initial prototype

- Controllers were 100 % dummy JSON stubs — every one is now wired to a service with real Pydantic bodies.
- SQLite/Postgres portability via a dialect-neutral GUID type.
- Rollback lost Bloom levels due to a `bloomsLevel`/`bloomLevel` key mismatch — normalised via `_row_from_dict`.
- `classify_many` sent 30–100 questions in one prompt and lost indices — chunked to 8, missing indices fall back per-question.
- DOCX had no image embedding, PDF didn't exist, parsing was fragile — reportlab PDF added, images embedded, lossless JSON footer added.
- Publish had no auth, no retries, no digest — Bearer token, jittered retries, SHA-256 digest column, demo-artifact fallback.
- Missing: submissions/immutability, planner-change propagation, teacher dashboard — all present as first-class features.

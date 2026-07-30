# API Reference

Base URL: `http://localhost:8000/api`
Envelope: every JSON response is `{ "success": bool, "message": str, "data": ... }`.

Error mapping (global exception handlers in `main.py`):

| Exception | HTTP |
|-----------|-----:|
| `LookupError` (entity not found) | 404 |
| `ValueError` (bad input) | 400 |
| `RuntimeError` (upstream / portal / model) | 502 |
| others | 500 |

---

## Curriculum

`GET /api/grades` — list all grades.

`GET /api/grades/{gradeId}/courses`

`GET /api/courses/{courseId}/units`

`GET /api/units/{unitId}/chapters`

`POST /api/curriculum`
```json
{ "gradeId": 8, "courseId": 101, "unitId": 12, "chapterId": 1201 }
```
Returns `{ curriculumId, chapterName }`.

`GET /api/curriculum/{curriculumId}/assessments` — chapter details + all assessments for it.

`GET /api/planners` — every planner (from Google Sheets or the bundled fallback).

`GET /api/planners/{plannerId}` — planner details plus every assessment generated against it.

---

## Assessments

`GET /api/assessments` — list.

`POST /api/assessments`
```json
{ "plannerId": "P004", "prompt": "Emphasise diagrams", "generatedBy": "SYSTEM" }
```
Body accepts `curriculumId` instead of `plannerId` — the service resolves to a planner.

`GET /api/assessments/{id}` — one assessment (without questions).

`GET /api/assessments/{id}/details` — alias of the above (for legacy clients).

`GET /api/assessments/{id}/questions` — all questions.

`POST /api/assessments/{id}/regenerate`
```json
{ "prompt": "More analysis-level questions", "updatedBy": "SYSTEM" }
```

`DELETE /api/assessments/{id}`

`GET /api/assessments/{id}/docx` — `FileResponse` (`.docx`).

`GET /api/assessments/{id}/pdf` — `FileResponse` (`.pdf`).

`POST /api/assessments/{id}/parse` — rewrites the DOCX and returns its parsed schema; `data.source` is `"metadata"` on lossless round-trip or `"regex"` for teacher-edited files.

`POST /api/assessments/{id}/publish`
```json
{ "updatedBy": "SYSTEM" }
```
Returns `{ assessment, receipt: { target, digest, mode, ... } }`. Mode is `"http"` when `PORTAL_PUBLISH_URL` is set, otherwise `"artifact"` (JSON written to `generated_documents/`).

`POST /api/assessments/{id}/rollback`
```json
{ "version": 1, "updatedBy": "SYSTEM" }
```
Rebuilds the assessment and its questions from the snapshot at that version — preserves `bloomsLevel`, `learningOutcomes`, `image`.

`GET /api/assessments/{id}/versions` — chronological version log.

`POST /api/assessments/{id}/questions` — add a question by hand (body is `QuestionInput`).

---

## Questions

`GET /api/questions/{id}`

`PUT /api/questions/{id}` — body is `QuestionPatch`; any subset of `question`, `answer`, `options`, `questionType`, `difficulty`, `bloomsLevel`, `learningOutcomes`, `marks`, `image`.

`DELETE /api/questions/{id}`

`POST /api/questions/{id}/regenerate` — body `{ prompt?, updatedBy? }`; rewrites question + answer + options.

`POST /api/questions/{id}/answer/regenerate` — same body; rewrites the answer only.

`POST /api/questions/{id}/images` — `multipart/form-data`, field name `files`; supports `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`. Images are downscaled to a 1200 px max dimension via Pillow, served at `/uploads/<filename>`.

`DELETE /api/images/{imageId}` — deletes both the file and the metadata row.

---

## Submissions (stretch — immutability)

`POST /api/assessments/{id}/submissions`
```json
{
    "studentId": "stu-42",
    "studentName": "Alice",
    "answers": [{ "questionNumber": 1, "answer": "Yes." }]
}
```
Auto-scores by exact match (case-insensitive). Freezes the current assessment view into `lockedSnapshot`.

`GET /api/assessments/{id}/submissions` — list; each row exposes its `lockedSnapshot`.

---

## Propagation (stretch — dynamic outcome propagation)

`POST /api/planners/{plannerId}/outcomes`
```json
{ "learningOutcomes": ["…", "…"], "updatedBy": "SYSTEM" }
```
Overlays the planner outcomes in memory (or in Sheets if wired), diffs against the previous list, marks every Published assessment for that planner as `Outdated`, and records a `PropagationEvent`.

`GET /api/propagation/events` — feed for the Propagation UI.

---

## Dashboard (stretch — teacher dashboard sync)

`GET /api/dashboard/summary`
```json
{
    "totals": { "assessments": 3, "published": 1, "outdated": 0, "submissions": 2, "propagationEvents": 1 },
    "statusBreakdown": { "Generated": 2, "Published": 1, "Parsed": 0, "Outdated": 0 },
    "averageTotalMarks": 25.0,
    "recentAssessments": [ ... ],
    "recentSubmissions": [ ... ]
}
```

---

## Static

- `/static/*` → serves files under `Question Bank/` (chapter images).
- `/uploads/*` → serves user-uploaded question images.
- `/downloads/*` → serves generated DOCX/PDF/portal-artifact files.

---

## Request/response schemas

Every request body is a `pydantic.BaseModel` with `alias_generator=camel` (see `schema.py`). Both `snake_case` and `camelCase` keys are accepted; responses are always camelCase.

Example `Assessment` response:
```json
{
    "assessmentId": "24355198-a7b2-4a24-a000-…",
    "plannerId": "P004",
    "curriculumId": "CURR004",
    "assessmentNumber": 1,
    "version": 2,
    "totalMarks": 15,
    "marks": 15,
    "status": "Generated",
    "grade": "Grade 8",
    "courseName": "Science",
    "unitName": "Human Body",
    "chapterName": "Digestive System",
    "learningOutcomes": ["Identify digestive organs", "Explain digestion", "Describe nutrient absorption"],
    "learningOutcomeCount": 3,
    "questionCount": 9,
    "validationReport": {
        "questionCount": 9, "expectedCount": 9, "totalMarks": 15,
        "expectedMarks": 15, "duplicateQuestions": [], "missingOutcomes": [],
        "needsReview": false
    },
    "publishTarget": null,
    "publishDigest": null,
    "publishedOn": null,
    "generatedBy": "SYSTEM",
    "generatedOn": "2026-07-30T17:45:00",
    "updatedBy": "SYSTEM",
    "updatedOn": "2026-07-30T17:45:00"
}
```

Example `AssessmentQuestion` response includes both `bloomLevel` and `bloomsLevel` — camelCase clients written against the previous version keep working.

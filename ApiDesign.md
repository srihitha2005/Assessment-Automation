# Assessment Automation Backend API Documentation

## Base URL

```
/api
```

---

# 1. Get All Grades

### Endpoint

```http
GET /grades
```

### Description

Returns all available grades.

### Request

No input required.

### Response

```json
{
  "totalGrades": 3,
  "grades": [
    {
      "gradeId": 1,
      "gradeName": "Grade 6",
      "numberOfUnits": 5
    },
    {
      "gradeId": 2,
      "gradeName": "Grade 7",
      "numberOfUnits": 6
    }
  ]
}
```

---

# 2. Get Courses by Grade

### Endpoint

```http
GET /grades/{gradeId}/courses
```

### Input

| Parameter | Type |
|-----------|------|
| gradeId | Integer |

### Response

```json
{
  "gradeId": 1,
  "numberOfCourses": 4,
  "courses": [
    {
      "courseId": 101,
      "courseName": "Science",
      "numberOfUnits": 5
    },
    {
      "courseId": 102,
      "courseName": "Mathematics",
      "numberOfUnits": 6
    }
  ]
}
```

---

# 3. Get Units by Course

### Endpoint

```http
GET /courses/{courseId}/units
```

### Input

| Parameter | Type |
|-----------|------|
| courseId | Integer |

### Response

```json
{
  "courseId": 101,
  "numberOfUnits": 5,
  "units": [
    {
      "unitId": 11,
      "unitName": "Human Body",
      "numberOfChapters": 6
    }
  ]
}
```

---

# 4. Get Chapters by Unit

### Endpoint

```http
GET /units/{unitId}/chapters
```

### Input

| Parameter | Type |
|-----------|------|
| unitId | Integer |

### Response

```json
{
  "unitId": 11,
  "numberOfChapters": 6,
  "chapters": [
    {
      "chapterId": 101,
      "chapterName": "Digestive System",
      "numberOfAssessments": 3
    }
  ]
}
```

---

# 5. Get Curriculum ID

### Endpoint

```http
POST /curriculum
```

### Request

```json
{
  "gradeId": 1,
  "courseId": 101,
  "unitId": 11,
  "chapterId": 101
}
```

### Response

```json
{
  "curriculumId": 55
}
```

---

# 6. Get Assessments by Curriculum

### Endpoint

```http
GET /curriculum/{curriculumId}/assessments
```

### Response

```json
{
  "curriculumId": 55,
  "learningOutcomes": [
    "Identify the organs of the digestive system.",
    "Explain the digestion process."
  ],
  "numberOfAssessments": 2,
  "assessments": [
    {
      "assessmentId": 1,
      "assessmentNumber": 1,
      "status": "Published",
      "marks": 50,
      "numberOfQuestions": 15
    }
  ]
}
```

---

# 7. Add Assessment

### Endpoint

```http
POST /assessments
```

### Request

```json
{
  "curriculumId": 55,
  "prompt": "Generate more application-based questions."
}
```

### Response

```json
{
  "success": true,
  "message": "Assessment generated successfully."
}
```

---

# 8. Delete Assessment

### Endpoint

```http
DELETE /assessments/{assessmentId}
```

### Response

```json
{
  "success": true,
  "message": "Assessment deleted successfully."
}
```

---

# 9. View Assessment Details

### Endpoint

```http
GET /assessments/{assessmentId}/details
```

### Response

```json
{
  "assessmentId": 1,
  "assessmentNumber": 2,
  "version": 3,
  "generatedOn": "2026-07-30",
  "generatedBy": "SYSTEM",
  "updatedOn": "2026-07-30",
  "updatedBy": "SYSTEM",
  "marks": 50,
  "numberOfQuestions": 15
}
```

---

# 10. View Assessment

### Endpoint

```http
GET /assessments/{assessmentId}
```

### Response

```json
{
  "assessmentId": 1,
  "questions": [
    {
      "questionId": 1001,
      "question": "What is digestion?",
      "answer": "Process of breaking down food.",
      "marks": 2
    }
  ]
}
```

---

# 11. Regenerate Assessment

### Endpoint

```http
POST /assessments/{assessmentId}/regenerate
```

### Request

```json
{
  "prompt": "Increase analytical questions."
}
```

### Response

```json
{
  "success": true,
  "message": "Assessment regenerated successfully."
}
```

---

# 12. Generate DOCX

### Endpoint

```http
GET /assessments/{assessmentId}/docx
```

### Description

Generates and downloads an editable DOCX version of the assessment.

### Response

Returns an editable `.docx` file.

---

# 13. Publish Assessment

### Endpoint

```http
POST /assessments/{assessmentId}/publish
```

### Response

```json
{
  "success": true,
  "message": "Assessment published successfully."
}
```

---

# 14. Rollback Assessment

### Endpoint

```http
POST /assessments/{assessmentId}/rollback
```

### Response

```json
{
  "success": true,
  "message": "Assessment rolled back successfully."
}
```

---

# 15. Generate More Questions

### Endpoint

```http
POST /assessments/{assessmentId}/questions/generate
```

### Response

```json
{
  "success": true,
  "message": "Additional questions generated successfully."
}
```

---

# 16. View Question

### Endpoint

```http
GET /questions/{questionId}
```

### Response

```json
{
  "questionId": 1001,
  "questionNumber": 3,
  "question": "What is digestion?",
  "questionType": "MCQ",
  "options": [
    "Option A",
    "Option B",
    "Option C",
    "Option D"
  ],
  "answer": "Option A",
  "marks": 2,
  "learningOutcome": "Explain digestion.",
  "difficulty": "Medium",
  "bloomLevel": "Understand"
}
```

---

# 17. Delete Question

### Endpoint

```http
DELETE /questions/{questionId}
```

### Response

```json
{
  "success": true,
  "message": "Question deleted successfully."
}
```

---

# 18. Edit Question

### Endpoint

```http
PUT /questions/{questionId}
```

### Request

```json
{
  "question": "Edited question",
  "answer": "Edited answer"
}
```

### Response

```json
{
  "success": true,
  "message": "Question updated successfully."
}
```

---

# 19. Regenerate Question

### Endpoint

```http
POST /questions/{questionId}/regenerate
```

### Request

```json
{
  "prompt": "Make it more application based."
}
```

### Response

```json
{
  "success": true,
  "message": "Question regenerated successfully."
}
```

---

# 20. Regenerate Answer

### Endpoint

```http
POST /questions/{questionId}/answer/regenerate
```

### Request

```json
{
  "prompt": "Provide a detailed answer."
}
```

### Response

```json
{
  "success": true,
  "message": "Answer regenerated successfully."
}
```

---

# 21. Rollback Question

### Endpoint

```http
POST /questions/{questionId}/rollback
```

### Response

```json
{
  "success": true,
  "message": "Question rolled back successfully."
}
```

---

# 22. Image Management

## Upload Image

### Endpoint

```http
POST /questions/{questionId}/images
```

### Request

Multipart Form Data

```
image[]
```

### Response

```json
{
  "success": true,
  "message": "Image uploaded successfully."
}
```

---

## Delete Image

### Endpoint

```http
DELETE /images/{imageId}
```

### Response

```json
{
  "success": true,
  "message": "Image deleted successfully."
}
```

---

# Backend Controller Structure

```
controller/

├── curriculum_controller.py
│   ├── GET /grades
│   ├── GET /grades/{gradeId}/courses
│   ├── GET /courses/{courseId}/units
│   ├── GET /units/{unitId}/chapters
│   ├── POST /curriculum
│   └── GET /curriculum/{curriculumId}/assessments
│
├── assessment_controller.py
│   ├── POST /assessments
│   ├── DELETE /assessments/{assessmentId}
│   ├── GET /assessments/{assessmentId}/details
│   ├── GET /assessments/{assessmentId}
│   ├── POST /assessments/{assessmentId}/regenerate
│   ├── GET /assessments/{assessmentId}/docx
│   ├── POST /assessments/{assessmentId}/publish
│   ├── POST /assessments/{assessmentId}/rollback
│   └── POST /assessments/{assessmentId}/questions/generate
│
├── question_controller.py
│   ├── GET /questions/{questionId}
│   ├── DELETE /questions/{questionId}
│   ├── PUT /questions/{questionId}
│   ├── POST /questions/{questionId}/regenerate
│   ├── POST /questions/{questionId}/answer/regenerate
│   ├── POST /questions/{questionId}/rollback
│   ├── POST /questions/{questionId}/images
│   └── DELETE /images/{imageId}
```

## Notes

- Google Sheets is the source of truth for Curriculum and Planner data.
- PostgreSQL stores Assessments, Questions, Versions and Metadata.
- Question Bank JSON files store reusable question templates.
- Ollama is used for question classification and fallback question generation.
- Generated questions are added back to the Question Bank for future reuse.
- Previous assessment questions are excluded from future assessment generation for the same curriculum whenever possible.
- DOCX generation produces an editable assessment document ready for download.
- Rollback restores the previous version of an assessment or question.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ /app/backend/
COPY ["Question Bank", "/app/Question Bank"]

WORKDIR /app/backend

ENV QUESTION_BANK_ROOT=/app/Question\ Bank \
    GENERATED_DOCUMENT_ROOT=/app/backend/generated_documents \
    UPLOADED_IMAGE_ROOT=/app/backend/uploaded_images

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

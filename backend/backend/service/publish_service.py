"""Direct portal integration.

Signs the assessment payload with SHA-256, POSTs it to
``settings.portal_publish_url`` with a Bearer token when configured, retries
transient failures with jittered exponential backoff, and — when no portal
URL is set — writes the signed payload to ``generated_documents/`` so the
demo has a real artifact to inspect.
"""
from __future__ import annotations

import hashlib
import json
import logging
import random
import time
from pathlib import Path

import requests

from config import settings

logger = logging.getLogger(__name__)


class PublishError(RuntimeError):
    """Raised when the portal rejects a publish after all retries."""


class PublishService:
    def publish(self, payload: dict) -> dict:
        """Publish an assessment and return a receipt."""
        body = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
        digest = hashlib.sha256(body).hexdigest()

        if not settings.portal_publish_url:
            path = self._write_demo_artifact(payload, body, digest)
            logger.info("PORTAL_PUBLISH_URL not set; wrote demo artifact %s", path)
            return {
                "target": path.as_posix(),
                "digest": digest,
                "mode": "artifact",
                "message": "PORTAL_PUBLISH_URL not configured — wrote demo artifact.",
            }

        headers = {"Content-Type": "application/json", "X-Content-Digest": f"sha256={digest}"}
        if settings.portal_api_key:
            headers["Authorization"] = f"Bearer {settings.portal_api_key}"

        last_error: Exception | None = None
        for attempt in range(1, settings.portal_max_retries + 1):
            try:
                response = requests.post(
                    settings.portal_publish_url,
                    data=body,
                    headers=headers,
                    timeout=settings.portal_timeout_seconds,
                )
                if 200 <= response.status_code < 300:
                    return {
                        "target": settings.portal_publish_url,
                        "digest": digest,
                        "mode": "http",
                        "status": response.status_code,
                        "response": self._response_snippet(response),
                    }
                last_error = PublishError(
                    f"Portal responded HTTP {response.status_code}: {response.text[:200]}"
                )
                if response.status_code < 500:
                    break  # 4xx won't get better with retries
            except requests.RequestException as error:
                last_error = error
            self._sleep(attempt)

        raise PublishError(f"Portal publish failed after {settings.portal_max_retries} attempts: {last_error}")

    def _write_demo_artifact(self, payload: dict, body: bytes, digest: str) -> Path:
        settings.generated_document_root.mkdir(parents=True, exist_ok=True)
        target = settings.generated_document_root / f"portal_{payload['assessmentId']}.json"
        wrapper = {
            "digest": {"algorithm": "sha256", "value": digest},
            "receivedAt": None,
            "payload": payload,
        }
        target.write_text(json.dumps(wrapper, ensure_ascii=False, indent=2), encoding="utf-8")
        return target

    @staticmethod
    def _response_snippet(response: requests.Response) -> str:
        try:
            return json.dumps(response.json())[:300]
        except ValueError:
            return response.text[:300]

    @staticmethod
    def _sleep(attempt: int) -> None:
        base = min(2 ** attempt, 30)
        time.sleep(base + random.uniform(0, base * 0.25))

"""End-to-end smoke test.

Runs against a live backend. Exercises every controller in the intended
demo order and prints a concise summary. Exit code 0 on full success.

Usage:
    python scripts/smoke_test.py                 # defaults to http://localhost:8000
    python scripts/smoke_test.py --url http://backend:8000
"""
from __future__ import annotations

import argparse
import json
import sys
import time

import requests


def _colour(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"


def ok(text: str) -> None:
    print(_colour(f"  [ok]{text}", "32"))


def info(text: str) -> None:
    print(_colour(f"  ..{text}", "36"))


def fail(text: str) -> None:
    print(_colour(f"  [x]{text}", "31"))


def run(base_url: str) -> None:
    session = requests.Session()

    print("-> health")
    r = session.get(f"{base_url}/", timeout=10)
    r.raise_for_status()
    ok("root endpoint responds")

    print("-> curriculum")
    r = session.get(f"{base_url}/api/grades", timeout=10)
    r.raise_for_status()
    grades = r.json()["data"]
    ok(f"grades: {grades['totalGrades']}")

    r = session.get(f"{base_url}/api/planners", timeout=10)
    r.raise_for_status()
    planners = r.json()["data"]
    ok(f"planners: {planners['totalPlanners']}")

    print("-> generate assessment for P004")
    r = session.post(
        f"{base_url}/api/assessments",
        json={"plannerId": "P004", "generatedBy": "SMOKE"},
        timeout=180,
    )
    r.raise_for_status()
    assessment = r.json()["data"]
    aid = assessment["assessmentId"]
    ok(f"assessment {aid} with {assessment['questionCount']} q / {assessment['totalMarks']} marks")

    print("-> fetch questions")
    r = session.get(f"{base_url}/api/assessments/{aid}/questions", timeout=10)
    r.raise_for_status()
    questions = r.json()["data"]
    ok(f"questions returned: {len(questions)}")

    print("-> update question")
    qid = questions[0]["questionId"]
    r = session.put(
        f"{base_url}/api/questions/{qid}",
        json={"question": "Smoke-updated question?", "answer": "Yes.", "marks": 3},
        timeout=10,
    )
    r.raise_for_status()
    ok("question updated")

    print("-> download DOCX")
    r = session.get(f"{base_url}/api/assessments/{aid}/docx", timeout=30)
    r.raise_for_status()
    ok(f"docx bytes: {len(r.content)}")

    print("-> download PDF")
    r = session.get(f"{base_url}/api/assessments/{aid}/pdf", timeout=30)
    r.raise_for_status()
    ok(f"pdf bytes: {len(r.content)}")

    print("-> parse (lossless)")
    r = session.post(f"{base_url}/api/assessments/{aid}/parse", timeout=30)
    r.raise_for_status()
    parsed = r.json()["data"]
    ok(f"parsed via '{parsed['source']}', {len(parsed['questions'])} questions round-tripped")

    print("-> publish")
    r = session.post(f"{base_url}/api/assessments/{aid}/publish", json={}, timeout=60)
    r.raise_for_status()
    receipt = r.json()["data"]["receipt"]
    ok(f"publish mode: {receipt['mode']}, digest {receipt['digest'][:16]}...")

    print("-> record submission")
    r = session.post(
        f"{base_url}/api/assessments/{aid}/submissions",
        json={"studentId": "stu-smoke", "studentName": "Smoke", "answers": []},
        timeout=10,
    )
    r.raise_for_status()
    submission = r.json()["data"]
    ok(f"submission {submission['submissionId'][:8]}... scored {submission['score']}/{submission['maxScore']}")

    print("-> list versions")
    r = session.get(f"{base_url}/api/assessments/{aid}/versions", timeout=10)
    r.raise_for_status()
    versions = r.json()["data"]
    ok(f"versions recorded: {len(versions)}")

    print("-> rollback")
    if len(versions) >= 2:
        target = versions[-1]["version"]
        r = session.post(
            f"{base_url}/api/assessments/{aid}/rollback",
            json={"version": target},
            timeout=30,
        )
        r.raise_for_status()
        ok(f"rolled back to v{target}")

    print("-> propagate planner change")
    r = session.post(
        f"{base_url}/api/planners/P004/outcomes",
        json={
            "learningOutcomes": [
                "Identify digestive organs",
                "Trace food through the body",
                "Describe nutrient absorption",
                "New outcome from smoke test",
            ]
        },
        timeout=10,
    )
    r.raise_for_status()
    event = r.json()["data"]
    ok(f"propagation event {event['eventId'][:8]}... added={len(event['addedOutcomes'])}")

    print("-> dashboard")
    r = session.get(f"{base_url}/api/dashboard/summary", timeout=10)
    r.raise_for_status()
    summary = r.json()["data"]
    ok(f"dashboard totals: {json.dumps(summary['totals'])}")

    print()
    print(_colour("All smoke checks passed.", "32"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8000", help="Backend base URL")
    parser.add_argument(
        "--wait", type=int, default=0, help="Seconds to wait before starting (for CI)",
    )
    args = parser.parse_args()
    if args.wait:
        time.sleep(args.wait)
    try:
        run(args.url.rstrip("/"))
    except requests.HTTPError as error:
        fail(f"HTTP {error.response.status_code}: {error.response.text[:200]}")
        return 1
    except requests.RequestException as error:
        fail(str(error))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

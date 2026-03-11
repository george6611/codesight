from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, Header, HTTPException, Request

from codesight.ai.provider import AIProvider
from codesight.analysis_engine import AnalysisEngine
from codesight.config import settings
from codesight.gitlab_client import GitLabClient
from codesight.scanners.registry import ScannerRegistry
from codesight.service import CodeSightService

app = FastAPI(title="CodeSight", version="0.1.0")

service = CodeSightService(
    scanner=ScannerRegistry(),
    analyzer=AnalysisEngine(ai_provider=AIProvider()),
    gitlab=GitLabClient(),
)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/scan")
async def scan_on_demand(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Manual local endpoint for quick testing.

    Example payload:
    {
      "repo_path": ".",
      "mr_iid": 42
    }
    """

    repo_path = Path(payload.get("repo_path", ".")).resolve()
    report = service.scan_repository(repo_path)

    mr_iid = payload.get("mr_iid")
    if mr_iid is not None:
        service.publish_to_merge_request(int(mr_iid), report)

    return {
        "summary": report.summary,
        "issues": [issue.__dict__ for issue in report.issues],
        "suggestions": [suggestion.__dict__ for suggestion in report.suggestions],
    }


@app.post("/webhook/gitlab")
async def handle_gitlab_webhook(
    request: Request,
    x_gitlab_token: str | None = Header(default=None),
    x_gitlab_event: str | None = Header(default=None),
) -> Dict[str, Any]:
    """Handles GitLab events for MR, pipeline, and custom scan triggers."""

    if settings.gitlab_webhook_secret and x_gitlab_token != settings.gitlab_webhook_secret:
        raise HTTPException(status_code=401, detail="Invalid webhook token")

    payload = await request.json()
    event = x_gitlab_event or payload.get("event_name", "")

    # In production, you usually clone the target branch before scanning.
    # This sample scans the local working directory for simplicity.
    repo_path = Path(".").resolve()
    report = service.scan_repository(repo_path)

    if event == "Merge Request Hook":
        mr = payload.get("object_attributes", {})
        mr_iid = mr.get("iid")
        if mr_iid:
            service.publish_to_merge_request(int(mr_iid), report)
        return {"status": "processed", "event": event, "summary": report.summary}

    if event == "Pipeline Hook":
        pipeline = payload.get("object_attributes", {})
        status = pipeline.get("status", "")
        if status == "failed":
            # Optional extension: map commit SHA to MR and comment there.
            return {"status": "processed", "event": event, "summary": report.summary}

    if event == "CodeSight Scan Request":
        issue_iid = payload.get("issue_iid")
        if issue_iid:
            service.publish_to_issue(int(issue_iid), report)
        return {"status": "processed", "event": event, "summary": report.summary}

    return {"status": "ignored", "event": event}

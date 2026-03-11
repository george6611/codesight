from pathlib import Path
from typing import List, Optional

from codesight.analysis_engine import AnalysisEngine
from codesight.config import settings
from codesight.gitlab_client import GitLabClient
from codesight.models import ScanReport
from codesight.scanners.registry import ScannerRegistry


class CodeSightService:
    """Main orchestration service for scanning, suggesting fixes, and publishing output."""

    def __init__(self, scanner: ScannerRegistry, analyzer: AnalysisEngine, gitlab: GitLabClient):
        self.scanner = scanner
        self.analyzer = analyzer
        self.gitlab = gitlab

    def scan_repository(self, repo_path: Path) -> ScanReport:
        issues = self.scanner.scan_repository(repo_path, max_files=settings.max_files_per_scan)
        suggestions = self.analyzer.suggest_fixes(issues) if issues else []

        summary = (
            f"Detected {len(issues)} issue(s). Generated {len(suggestions)} suggestion(s)."
        )
        return ScanReport(issues=issues, suggestions=suggestions, summary=summary)

    def publish_to_merge_request(self, mr_iid: int, report: ScanReport) -> None:
        if not settings.comment_on_mr:
            return

        body = self._render_report_comment(report)
        self.gitlab.post_mr_comment(mr_iid, body)

    def publish_to_issue(self, issue_iid: int, report: ScanReport) -> None:
        body = self._render_report_comment(report)
        self.gitlab.post_issue_comment(issue_iid, body)

    def create_draft_fix_mr(
        self,
        branch_name: str,
        target_branch: str,
        title: str,
        description: str,
    ) -> dict:
        return self.gitlab.create_merge_request(
            source_branch=branch_name,
            target_branch=target_branch,
            title=title,
            description=description,
            draft=True,
        )

    @staticmethod
    def _render_report_comment(report: ScanReport) -> str:
        lines: List[str] = ["## CodeSight Scan Results", "", report.summary or ""]

        if not report.issues:
            lines.append("No issues detected.")
            return "\n".join(lines)

        for index, issue in enumerate(report.issues, start=1):
            lines.extend(
                [
                    f"### Issue {index}",
                    f"- File: `{issue.file_path}`",
                    f"- Line: `{issue.line}`",
                    f"- Severity: `{issue.severity}`",
                    f"- Type: `{issue.issue_type}`",
                    f"- Message: {issue.message}",
                ]
            )

            match = next(
                (s for s in report.suggestions if s.file_path == issue.file_path and s.issue_message == issue.message),
                None,
            )
            if match:
                lines.extend(
                    [
                        "- Suggested fix:",
                        f"  - {match.explanation}",
                        "```diff",
                        match.patch,
                        "```",
                    ]
                )

            lines.append("")

        return "\n".join(lines)

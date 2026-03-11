import argparse
from pathlib import Path

from codesight.ai.provider import AIProvider
from codesight.analysis_engine import AnalysisEngine
from codesight.gitlab_client import GitLabClient
from codesight.scanners.registry import ScannerRegistry
from codesight.service import CodeSightService


def main() -> None:
    """Example script to scan a repository directory locally."""

    parser = argparse.ArgumentParser(description="Run CodeSight local scan")
    parser.add_argument("--repo", default=".", help="Path to repository directory")
    parser.add_argument("--mr", type=int, default=None, help="Optional MR IID to post results")
    args = parser.parse_args()

    service = CodeSightService(
        scanner=ScannerRegistry(),
        analyzer=AnalysisEngine(ai_provider=AIProvider()),
        gitlab=GitLabClient(),
    )

    report = service.scan_repository(Path(args.repo).resolve())
    print(report.summary)

    for issue in report.issues:
        print(f"- {issue.file_path}:{issue.line} [{issue.severity}] {issue.message}")

    if args.mr is not None:
        service.publish_to_merge_request(args.mr, report)
        print(f"Posted comment to MR !{args.mr}")


if __name__ == "__main__":
    main()

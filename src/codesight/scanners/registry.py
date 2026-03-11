from pathlib import Path
from typing import Iterable, List

from codesight.models import Issue
from codesight.scanners.base import BaseScanner
from codesight.scanners.javascript_scanner import JavaScriptScanner
from codesight.scanners.python_scanner import PythonScanner


class ScannerRegistry:
    """Coordinates multiple language scanners over repository files."""

    def __init__(self) -> None:
        self.scanners: List[BaseScanner] = [PythonScanner(), JavaScriptScanner()]

    def scan_repository(self, repo_path: Path, max_files: int = 300) -> List[Issue]:
        issues: List[Issue] = []
        files_scanned = 0

        for file_path in repo_path.rglob("*"):
            if not file_path.is_file():
                continue
            if "/.git/" in str(file_path).replace("\\", "/"):
                continue

            for scanner in self.scanners:
                if scanner.can_scan(file_path):
                    issues.extend(scanner.scan_file(file_path))
                    files_scanned += 1
                    break

            if files_scanned >= max_files:
                break

        return issues

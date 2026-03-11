import shutil
import subprocess
from pathlib import Path
from typing import List

from codesight.models import Issue
from codesight.scanners.base import BaseScanner


class JavaScriptScanner(BaseScanner):
    """Runs a lightweight syntax validation for JS files using Node.js."""

    def can_scan(self, file_path: Path) -> bool:
        return file_path.suffix in {".js", ".mjs", ".cjs"}

    def scan_file(self, file_path: Path) -> List[Issue]:
        issues: List[Issue] = []
        if shutil.which("node") is None:
            return issues

        # This command asks Node to parse the file without executing it.
        cmd = ["node", "--check", str(file_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            message = (result.stderr or result.stdout).strip()
            issues.append(
                Issue(
                    file_path=str(file_path),
                    line=1,
                    column=1,
                    severity="high",
                    issue_type="syntax_error",
                    message=message,
                    code_snippet="",
                )
            )
        return issues

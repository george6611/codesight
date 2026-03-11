import ast
from pathlib import Path
from typing import List

from codesight.models import Issue
from codesight.scanners.base import BaseScanner


class PythonScanner(BaseScanner):
    """Detects Python syntax errors and simple quality issues."""

    def can_scan(self, file_path: Path) -> bool:
        return file_path.suffix == ".py"

    def scan_file(self, file_path: Path) -> List[Issue]:
        issues: List[Issue] = []
        source = file_path.read_text(encoding="utf-8", errors="ignore")

        try:
            tree = ast.parse(source)
        except SyntaxError as err:
            issues.append(
                Issue(
                    file_path=str(file_path),
                    line=err.lineno or 1,
                    column=err.offset or 1,
                    severity="high",
                    issue_type="syntax_error",
                    message=str(err.msg),
                    code_snippet=self._extract_line(source, err.lineno or 1),
                )
            )
            return issues

        # Simple example rule: detect bare "except:" blocks.
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                line = getattr(node, "lineno", 1)
                issues.append(
                    Issue(
                        file_path=str(file_path),
                        line=line,
                        column=1,
                        severity="medium",
                        issue_type="bug_risk",
                        message="Bare except found. Catch specific exceptions instead.",
                        code_snippet=self._extract_line(source, line),
                    )
                )

        return issues

    @staticmethod
    def _extract_line(source: str, line_number: int) -> str:
        lines = source.splitlines()
        if 1 <= line_number <= len(lines):
            return lines[line_number - 1].strip()
        return ""

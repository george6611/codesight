from pathlib import Path
from typing import List

from codesight.ai.prompts import build_fix_prompt
from codesight.ai.provider import AIProvider
from codesight.models import FixSuggestion, Issue


class AnalysisEngine:
    """Converts scanner issues into AI-backed fix suggestions."""

    def __init__(self, ai_provider: AIProvider) -> None:
        self.ai_provider = ai_provider

    def suggest_fixes(self, issues: List[Issue]) -> List[FixSuggestion]:
        suggestions: List[FixSuggestion] = []

        for issue in issues:
            file_content = ""
            path = Path(issue.file_path)
            if path.exists():
                file_content = path.read_text(encoding="utf-8", errors="ignore")

            prompt = build_fix_prompt(issue, file_content)
            model_output = self.ai_provider.generate_fix(prompt)
            explanation, patch = self._parse_model_output(model_output)

            suggestions.append(
                FixSuggestion(
                    file_path=issue.file_path,
                    issue_message=issue.message,
                    explanation=explanation,
                    patch=patch,
                )
            )

        return suggestions

    @staticmethod
    def _parse_model_output(model_output: str) -> tuple[str, str]:
        explanation = model_output
        patch = ""

        if "PATCH:" in model_output:
            parts = model_output.split("PATCH:", 1)
            explanation = parts[0].replace("EXPLANATION:", "").strip()
            patch = parts[1].strip()

        return explanation, patch

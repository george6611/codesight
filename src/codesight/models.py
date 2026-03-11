from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Issue:
    """Represents a single detected code problem."""

    file_path: str
    line: int
    column: int
    severity: str
    issue_type: str
    message: str
    code_snippet: str = ""


@dataclass
class FixSuggestion:
    """Represents an AI-generated fix for a specific issue."""

    file_path: str
    issue_message: str
    explanation: str
    patch: str


@dataclass
class ScanReport:
    """Aggregates scanner findings and AI suggestions."""

    issues: List[Issue] = field(default_factory=list)
    suggestions: List[FixSuggestion] = field(default_factory=list)
    summary: Optional[str] = None

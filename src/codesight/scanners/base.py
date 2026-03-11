from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from codesight.models import Issue


class BaseScanner(ABC):
    """Abstract scanner interface for language-specific analyzers."""

    @abstractmethod
    def can_scan(self, file_path: Path) -> bool:
        """Returns True if this scanner supports the given file."""

    @abstractmethod
    def scan_file(self, file_path: Path) -> List[Issue]:
        """Scans one file and returns detected issues."""

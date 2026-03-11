from pathlib import Path


def strip_diff_fences(text: str) -> str:
    """Removes markdown code fences around diff text when present."""

    cleaned = text.strip()
    if cleaned.startswith("```diff"):
        cleaned = cleaned[len("```diff") :]
    if cleaned.endswith("```"):
        cleaned = cleaned[: -len("```")]
    return cleaned.strip()


def apply_simple_replace_patch(file_path: Path, old: str, new: str) -> bool:
    """Applies a minimal text replacement patch for demo purposes.

    This utility is intentionally simple so local testing is easy.
    For production, use a robust unified-diff parser library.
    """

    if not file_path.exists():
        return False

    source = file_path.read_text(encoding="utf-8", errors="ignore")
    if old not in source:
        return False

    updated = source.replace(old, new, 1)
    file_path.write_text(updated, encoding="utf-8")
    return True

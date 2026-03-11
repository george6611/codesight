from pathlib import Path

from codesight.scanners.python_scanner import PythonScanner


def test_detects_python_syntax_error(tmp_path: Path) -> None:
    file_path = tmp_path / "broken.py"
    file_path.write_text("def bad(:\n    pass\n", encoding="utf-8")

    scanner = PythonScanner()
    issues = scanner.scan_file(file_path)

    assert issues
    assert issues[0].issue_type == "syntax_error"

from codesight.models import Issue


def build_fix_prompt(issue: Issue, file_content: str) -> str:
    """Builds a concise prompt asking the model for explanation and patch output."""

    return f"""
You are a code review assistant.

Task:
1) Explain the problem in plain language.
2) Suggest a fix.
3) Return a unified diff patch.

Issue details:
- File: {issue.file_path}
- Line: {issue.line}
- Type: {issue.issue_type}
- Severity: {issue.severity}
- Message: {issue.message}

Current file content:
```text
{file_content}
```

Output format:
EXPLANATION:
<short explanation>

PATCH:
```diff
<unified diff patch>
```
""".strip()

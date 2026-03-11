# CodeSight - GitLab AI Code Fixer

CodeSight is an example GitLab Duo-style agent project that detects common coding issues, asks an AI model for fix suggestions, and posts results to GitLab as comments or draft merge requests.

## What It Does

- Scans repository files for common issues:
  - Python syntax and basic lint-style checks.
  - JavaScript syntax checks (if `node` is available).
- Uses an AI provider (OpenAI-compatible, Hugging Face Inference, or local endpoint) to:
  - Explain detected problems.
  - Suggest patch-style fixes.
- Integrates with GitLab APIs to:
  - Comment on merge requests and issues.
  - Create branches, commit fixes, and open draft merge requests.
- Supports trigger patterns for:
  - Merge request events.
  - Pipeline failure events.
  - On-demand scan requests.

## Project Structure

```text
codesight/
  config/
    duo-agent.yaml
  scripts/
    run_local_scan.py
    create_mr_example.py
    post_comment_example.py
  src/codesight/
    ai/
    scanners/
    analysis_engine.py
    config.py
    gitlab_client.py
    main.py
    service.py
  tests/
  .env.example
  .gitlab-ci.yml
  requirements.txt
```

## Quick Start (Local)

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy environment template and fill values:

```bash
cp .env.example .env
```

4. Run a local scan:

```bash
python scripts/run_local_scan.py --repo .
```

5. Start webhook service (for MR/pipeline triggers):

```bash
uvicorn src.codesight.main:app --host 0.0.0.0 --port 8000 --reload
```

## Trigger Flow

1. GitLab sends a webhook (`merge_request`, `pipeline`, or custom event).
2. CodeSight clones/reads repository files.
3. Scanner detects issues and sends context to AI provider.
4. Agent posts suggestions to MR/issues or creates a draft MR with fixes.

## GitLab Integration Setup

Set these environment variables:

- `GITLAB_URL` (example: `https://gitlab.com`)
- `GITLAB_TOKEN` (personal access token or bot token)
- `GITLAB_PROJECT_ID` (numeric project ID)

Optional:

- `GITLAB_WEBHOOK_SECRET`

## AI Provider Setup

Set `MODEL_PROVIDER` as one of:

- `openai`
- `huggingface`
- `local`

Then configure endpoint/token variables in `.env`.

## GitLab Duo Agent Configuration

`config/duo-agent.yaml` contains an example deployment configuration and trigger mapping.
Use it as a template and adjust keys to your specific GitLab Duo Agent Platform version.

## Notes

- This repository is intentionally beginner-friendly and heavily documented.
- Production hardening ideas are listed at the bottom of `config/duo-agent.yaml` and in source comments.

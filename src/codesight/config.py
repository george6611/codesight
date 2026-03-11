import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    """Centralized runtime settings loaded from environment variables."""

    gitlab_url: str = os.getenv("GITLAB_URL", "https://gitlab.com")
    gitlab_token: str = os.getenv("GITLAB_TOKEN", "")
    gitlab_project_id: str = os.getenv("GITLAB_PROJECT_ID", "")
    gitlab_webhook_secret: str = os.getenv("GITLAB_WEBHOOK_SECRET", "")

    model_provider: str = os.getenv("MODEL_PROVIDER", "openai")
    model_name: str = os.getenv("MODEL_NAME", "gpt-4.1-mini")

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    huggingface_api_token: str = os.getenv("HUGGINGFACE_API_TOKEN", "")
    huggingface_model_id: str = os.getenv(
        "HUGGINGFACE_MODEL_ID", "meta-llama/Meta-Llama-3-8B-Instruct"
    )

    local_model_url: str = os.getenv(
        "LOCAL_MODEL_URL", "http://localhost:11434/v1/chat/completions"
    )
    local_model_token: str = os.getenv("LOCAL_MODEL_TOKEN", "")

    max_files_per_scan: int = int(os.getenv("MAX_FILES_PER_SCAN", "300"))
    auto_create_mr: bool = os.getenv("AUTO_CREATE_MR", "false").lower() == "true"
    comment_on_mr: bool = os.getenv("COMMENT_ON_MR", "true").lower() == "true"


settings = Settings()

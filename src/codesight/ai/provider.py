import json
from typing import Dict

import requests

from codesight.config import settings


class AIProvider:
    """Provider wrapper for OpenAI-compatible, Hugging Face, or local model calls."""

    def generate_fix(self, prompt: str) -> str:
        provider = settings.model_provider.lower()
        if provider == "openai":
            return self._call_openai(prompt)
        if provider == "huggingface":
            return self._call_huggingface(prompt)
        if provider == "local":
            return self._call_local(prompt)
        raise ValueError(f"Unsupported MODEL_PROVIDER: {settings.model_provider}")

    def _call_openai(self, prompt: str) -> str:
        url = f"{settings.openai_base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        }
        payload: Dict = {
            "model": settings.model_name,
            "messages": [
                {"role": "system", "content": "You are a senior software engineer."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.1,
        }
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    def _call_huggingface(self, prompt: str) -> str:
        url = (
            "https://api-inference.huggingface.co/models/"
            f"{settings.huggingface_model_id}"
        )
        headers = {
            "Authorization": f"Bearer {settings.huggingface_api_token}",
            "Content-Type": "application/json",
        }
        payload = {"inputs": prompt, "parameters": {"temperature": 0.1, "max_new_tokens": 800}}
        response = requests.post(url, headers=headers, json=payload, timeout=90)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and data and "generated_text" in data[0]:
            return data[0]["generated_text"]
        return json.dumps(data)

    def _call_local(self, prompt: str) -> str:
        headers = {"Content-Type": "application/json"}
        if settings.local_model_token:
            headers["Authorization"] = f"Bearer {settings.local_model_token}"

        payload: Dict = {
            "model": settings.model_name,
            "messages": [
                {"role": "system", "content": "You are a senior software engineer."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.1,
        }
        response = requests.post(
            settings.local_model_url,
            headers=headers,
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

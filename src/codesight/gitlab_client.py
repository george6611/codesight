from typing import Dict

import requests

from codesight.config import settings


class GitLabClient:
    """Minimal GitLab REST API wrapper for comments and merge requests."""

    def __init__(self) -> None:
        self.base_url = settings.gitlab_url.rstrip("/")
        self.project_id = settings.gitlab_project_id
        self.headers = {
            "PRIVATE-TOKEN": settings.gitlab_token,
            "Content-Type": "application/json",
        }

    def post_mr_comment(self, mr_iid: int, comment: str) -> Dict:
        url = (
            f"{self.base_url}/api/v4/projects/{self.project_id}/merge_requests/"
            f"{mr_iid}/notes"
        )
        response = requests.post(url, headers=self.headers, json={"body": comment}, timeout=30)
        response.raise_for_status()
        return response.json()

    def post_issue_comment(self, issue_iid: int, comment: str) -> Dict:
        url = f"{self.base_url}/api/v4/projects/{self.project_id}/issues/{issue_iid}/notes"
        response = requests.post(url, headers=self.headers, json={"body": comment}, timeout=30)
        response.raise_for_status()
        return response.json()

    def create_branch(self, branch_name: str, ref: str = "main") -> Dict:
        url = f"{self.base_url}/api/v4/projects/{self.project_id}/repository/branches"
        payload = {"branch": branch_name, "ref": ref}
        response = requests.post(url, headers=self.headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def commit_file(
        self,
        branch: str,
        file_path: str,
        content: str,
        commit_message: str,
    ) -> Dict:
        url = f"{self.base_url}/api/v4/projects/{self.project_id}/repository/commits"
        payload = {
            "branch": branch,
            "commit_message": commit_message,
            "actions": [
                {
                    "action": "update",
                    "file_path": file_path,
                    "content": content,
                }
            ],
        }
        response = requests.post(url, headers=self.headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def create_merge_request(
        self,
        source_branch: str,
        target_branch: str,
        title: str,
        description: str,
        draft: bool = True,
    ) -> Dict:
        url = f"{self.base_url}/api/v4/projects/{self.project_id}/merge_requests"
        payload = {
            "source_branch": source_branch,
            "target_branch": target_branch,
            "title": f"Draft: {title}" if draft else title,
            "description": description,
            "remove_source_branch": True,
        }
        response = requests.post(url, headers=self.headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

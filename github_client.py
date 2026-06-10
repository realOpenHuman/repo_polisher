import base64
import requests
from dotenv import load_dotenv
import os
load_dotenv()

class GitHubClient:
    def __init__(self, token: str | None = None):
        self.token = token
        self.base_url = "https://api.github.com"

    def _headers(self) -> dict:
        headers = {
            "Accept": "application/vnd.github+json"
        }

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        return headers

    def get_repo_info(self, owner: str, repo: str) -> dict:
        url = f"{self.base_url}/repos/{owner}/{repo}"

        response = requests.get(url, headers=self._headers())
        response.raise_for_status()

        return response.json()

    def get_default_branch(self, owner: str, repo: str) -> str:

        repo_info = self.get_repo_info(owner, repo)
        return repo_info["default_branch"]

    def get_file_tree(self, owner: str, repo: str, branch: str) -> list[dict]:
        url = f"{self.base_url}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"

        response = requests.get(url, headers=self._headers())
        response.raise_for_status()

        data = response.json()
        return data.get("tree", [])

    def read_file(self, owner: str, repo: str, path: str, branch: str) -> str:
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"

        params = {
            "ref": branch
        }

        response = requests.get(
            url,
            headers=self._headers(),
            params=params
        )
        response.raise_for_status()

        data = response.json()

        content = data["content"]
        encoding = data.get("encoding")

        if encoding == "base64":
            return base64.b64decode(content).decode("utf-8", errors="ignore")

        return content

    def get_file_sha(
        self,
        owner: str,
        repo: str,
        path: str,
        branch: str
    ) -> str | None:
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"

        params = {
            "ref": branch
        }

        response = requests.get(
            url,
            headers=self._headers(),
            params=params
        )

        if response.status_code == 404:
            return None

        response.raise_for_status()

        data = response.json()
        return data.get("sha")

    def create_or_update_file(
        self,
        owner: str,
        repo: str,
        path: str,
        content: str,
        message: str,
        branch: str
    ) -> dict:
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"

        file_sha = self.get_file_sha(
            owner=owner,
            repo=repo,
            path=path,
            branch=branch
        )

        encoded_content = base64.b64encode(
            content.encode("utf-8")
        ).decode("utf-8")

        payload = {
            "message": message,
            "content": encoded_content,
            "branch": branch
        }

        if file_sha:
            payload["sha"] = file_sha

        response = requests.put(
            url,
            headers=self._headers(),
            json=payload
        )
        response.raise_for_status()

        return response.json()
    def list_user_repos(self, username: str | None = None) -> list[str]:

        if username:
            url = f"{self.base_url}/users/{username}/repos"
        else:
            url = f"{self.base_url}/user/repos"

        params = {
            "per_page": 100,
            "sort": "updated"
        }

        response = requests.get(
            url,
            headers=self._headers(),
            params=params
        )

        if response.status_code >= 400:
            print("GitHub API Error:")
            print("status:", response.status_code)
            print("response:", response.text)

        response.raise_for_status()

        repos = response.json()

        return [repo["name"] for repo in repos]


if __name__ == "__main__":
    from repo_parser import parse_github_repo_url

    load_dotenv()
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    repo_info = parse_github_repo_url(
        "https://github.com/owner/repo"
    )

    github = GitHubClient(token=GITHUB_TOKEN)

    branch = repo_info["branch"] or github.get_default_branch(
        repo_info["owner"],
        repo_info["repo"]
    )

    print("owner:", repo_info["owner"])
    print("repo:", repo_info["repo"])
    print("branch:", branch)

    tree = github.get_file_tree(
        owner=repo_info["owner"],
        repo=repo_info["repo"],
        branch=branch
    )

    print("file count:", len(tree))

    for item in tree[:10]:
        print(item["path"], item["type"])
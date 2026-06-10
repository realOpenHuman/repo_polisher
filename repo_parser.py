from urllib.parse import urlparse
def parse_github_repo_url(github_url: str) -> dict:
    """
    {
        "owner": "owner",
        "repo": "repo",
        "branch": "main" 或 None,
        "repo_url": "https://github.com/owner/repo"
    }
    """

    github_url = github_url.strip()

    if github_url.startswith("git@github.com:"):
        path = github_url.replace("git@github.com:", "")
        path = path.replace(".git", "")
        owner, repo = path.split("/")[:2]

        return {
            "owner": owner,
            "repo": repo,
            "branch": None,
            "repo_url": f"https://github.com/{owner}/{repo}",
        }

    parsed = urlparse(github_url)
    parts = parsed.path.strip("/").split("/")

    owner = parts[0]
    repo = parts[1].replace(".git", "")

    branch = None

    if len(parts) >= 4 and parts[2] == "tree":
        branch = parts[3]

    return {
        "owner": owner,
        "repo": repo,
        "branch": branch,
        "repo_url": f"https://github.com/{owner}/{repo}",
    }

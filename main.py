from repo_parser import parse_github_repo_url
from github_client import GitHubClient
from readmemaker import make_readme
from dotenv import load_dotenv
import os
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
def main(github_url):
    repo_info = parse_github_repo_url(github_url)

    github = GitHubClient(token=GITHUB_TOKEN)

    branch = repo_info["branch"] or github.get_default_branch(
        owner=repo_info["owner"],
        repo=repo_info["repo"]
    )

    print("repo:", repo_info["repo_url"])
    print("branch:", branch)

    file_tree = github.get_file_tree(
        owner=repo_info["owner"],
        repo=repo_info["repo"],
        branch=branch
    )

    valid_files = [
        item for item in file_tree
        if item["type"] == "blob"
        and (
            item["path"].endswith(".py")
            or item["path"].endswith(".js")
            or item["path"].endswith(".ts")
            or item["path"].endswith(".json")
            or item["path"].endswith(".md")
            or item["path"].endswith(".txt")
            or item["path"].endswith(".env")
            or item["path"] in [
                "requirements.txt",
                "package.json",
                "pyproject.toml",
                "Dockerfile",
                "LICENSE",
            ]
        )
    ]

    print("\nvalid files:")
    for file in valid_files:
        print(file["path"])

    print("\nreading files...")

    repo_files = []

    for file in valid_files[:10]:
        path = file["path"]

        try:
            content = github.read_file(
                owner=repo_info["owner"],
                repo=repo_info["repo"],
                path=path,
                branch=branch
            )

            repo_files.append({
                "path": path,
                "content": content
            })

            print(f"read success: {path}")

        except Exception as e:
            print(f"read failed: {path} | {e}")

    print("\nloaded file count:", len(repo_files))
    generated_readme = make_readme(str(repo_files))
    github.create_or_update_file(
        owner=repo_info["owner"],
        repo=repo_info["repo"],
        path="README.md",
        content=generated_readme,
        message="docs: add generated README",
        branch=branch
    )

if __name__ == "__main__":
    print("输入仓库 URL 则仅针对该仓库，输入用户名则针对用户下所有公开仓库")

    input_value = input("请输入 GitHub 仓库 URL 或 GitHub 用户名：").strip()

    if input_value.startswith("http"):
        main(input_value)

    else:
        github = GitHubClient(token=GITHUB_TOKEN)

        repos = github.list_user_repos(username=input_value)

        for repo in repos:
            repo_url = f"https://github.com/{input_value}/{repo}"
            print(f"\n正在处理仓库：{repo_url}")
            main(repo_url)
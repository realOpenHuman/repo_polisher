# Repo Polisher

An AI-powered tool that automatically generates polished README.md files for GitHub repositories and commits them directly.

## Overview

Repo Polisher helps open-source maintainers and developers who want better documentation but don't have time to write it. Given a GitHub repository URL or a username, the tool analyzes key project files (source code, configs, documentation), uses a large language model to generate a well-structured README, and pushes the result as a commit to the repository.

The tool is designed to handle both individual repos and bulk updates across all public repos of a user.

## Features

- Parse GitHub repository URLs (including SSH and branch-specific URLs)
- Fetch and read critical project files: `.py`, `.js`, `.ts`, `.json`, `.md`, `.txt`, `.env`, `requirements.txt`, `package.json`, `pyproject.toml`, `Dockerfile`, `LICENSE`
- Generate a README using the DeepSeek API and a detailed prompt that follows best practices
- Commit the generated README directly to the repository (creates or updates `README.md`)
- Batch mode: process all public repositories of a given GitHub user

## Tech Stack

- **Language:** Python 3
- **API Clients:** `requests` for GitHub, `openai` for DeepSeek
- **Configuration:** `python-dotenv` for environment variables
- **LLM Backend:** DeepSeek (model `deepseek-v4-pro`)

## Project Structure

```
.
├── main.py              # CLI entry point; handles single and batch repo processing
├── github_client.py     # Wrapper around GitHub REST API (files, trees, commits)
├── repo_parser.py       # Extracts owner, repo, branch from GitHub URLs
├── readmemaker.py       # Calls DeepSeek API with a base prompt to generate README
├── readmemaker.md       # System prompt for the README generation agent
└── LICENSE              # MIT license
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- A GitHub [personal access token](https://github.com/settings/tokens) with `repo` scope
- A DeepSeek API key (from [DeepSeek](https://platform.deepseek.com/))

### Installation

Clone the repository and install the required Python dependencies.

```bash
git clone https://github.com/realOpenHuman/repo_polisher.git
cd repo_polisher
pip install requests python-dotenv openai
```

The project does not currently include a `requirements.txt` file. Create one with the above packages, or install them directly.

### Configuration

Create a `.env` file in the project root with the following variables:

```
GITHUB_TOKEN=your_github_personal_access_token
DEEPSEEK_API_KEY=your_deepseek_api_key
```

Both tokens are required. The GitHub token needs write access if you want the tool to commit the generated README.

### Running the Project

Start the interactive CLI:

```bash
python main.py
```

You will be prompted to enter either:
- A full GitHub repository URL (e.g., `https://github.com/owner/repo`)
- A GitHub username (to process all public repositories of that user)

The tool will analyze the target repositories, generate README files, and commit them.

## Usage

### Process a single repository

```
$ python main.py
输入仓库 URL 则仅针对该仓库，输入用户名则针对用户下所有公开仓库
请输入 GitHub 仓库 URL 或 GitHub 用户名：https://github.com/owner/repo
repo: https://github.com/owner/repo
branch: main

valid files:
package.json
src/index.js
README.md
LICENSE

reading files...
read success: package.json
read success: src/index.js
read success: README.md
read success: LICENSE

loaded file count: 4
```

The generated README is then pushed to the repository.

### Process all public repos of a user

```
$ python main.py
请输入 GitHub 仓库 URL 或 GitHub 用户名：someuser
正在处理仓库：https://github.com/someuser/repo1
... (processing)
正在处理仓库：https://github.com/someuser/repo2
...
```

## Limitations

- The tool reads only up to 10 valid files per repository to stay within typical content limits.
- File type filtering is hardcoded (`.py`, `.js`, `.ts`, `.json`, `.md`, `.txt`, `.env`, and certain configuration files). Other file types are ignored.
- The quality of the generated README depends on the content available in those 10 files and the AI model’s understanding.
- Batch processing of a user's repositories may hit GitHub API rate limits if the user has many repos.
- No local dry-run mode: the tool commits directly. Use caution when running against production repositories.

## Roadmap

Based on the repository structure, there is no explicit roadmap or issue tracker. Potential improvements could include:
- Support for more file types and smarter file selection
- A dry-run flag that prints the generated README without committing
- A `requirements.txt` or `pyproject.toml` for easier installation
- Unit tests

## Contributing

Contributions are welcome. To set up the project locally, follow the installation instructions above. Since there are no formal contribution guidelines, consider opening an issue first to discuss major changes.

This project does not currently have test suites or CI/CD pipelines. If you add tests, include clear instructions for running them.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

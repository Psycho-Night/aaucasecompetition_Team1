import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "Devershi_P"
REPO_NAME = "pull-request"
HEAD_BRANCH = "main"
BASE_BRANCH = "Devershi"

def create_pull_request():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    data = {
        "title": "Automated Pull Request: Feature Updates",
        "body": "This PR contains automated changes.",
        "head": HEAD_BRANCH,
        "base": BASE_BRANCH
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print("Pull request created successfully!")
    else:
        print("Failed to create PR:", response.json())

if __name__ == "__main__":
    create_pull_request()

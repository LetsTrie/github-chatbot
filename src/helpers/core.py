from .fetch_github_count import fetch_github_count
from .get_commits import get_commits, generate_commits_markdown
from .get_pull_requests import get_pull_requests, generate_pull_requests_markdown

async def get_count(action, params):   
    if action in ["commits", "pulls", "issues"]:
        return await fetch_github_count(action, params)

    return "No Response"

async def get_multiple_documents(action, params):
    # if action == "commits" or action == "pulls" or action == "issues":
    if action == "commits":
        commits = await get_commits(params)
        return generate_commits_markdown(commits)

    elif action == "pulls": 
        pulls = await get_pull_requests(params)
        return generate_pull_requests_markdown(pulls)

    return "No Response"
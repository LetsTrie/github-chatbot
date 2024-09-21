import aiohttp
import logging
from GithubUrlManager import GithubUrlManager

async def get_repository():
    github_url_manager = GithubUrlManager()
    metadata = github_url_manager.get_metadata()
        
    url = f"https://api.github.com/repos/{metadata.get('owner')}/{metadata.get('repo')}"
    logging.info(f"Fetching data from {url}")

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                repository = await response.json()
                return {
                    "name": repository.get("name"),
                    "description": repository.get("description"),
                    "visibility": "private" if repository.get("private") else "public",
                    "owner": repository["owner"].get("login"),
                    "homepage": repository.get("homepage"),
                    "created_at": repository.get("created_at"),
                    "last_pushed": repository.get("pushed_at"),
                    "default_branch": repository.get("default_branch"),
                    "stars": repository.get("stargazers_count"),
                    "watchers": repository.get("watchers_count"),
                    "subscribers": repository.get("subscribers_count"),
                    "forks": repository.get("forks_count"),
                    "open_issues": repository.get("open_issues_count"),
                    "language": repository.get("language"),
                    "license": repository.get("license", {}).get("name"),
                }

            logging.error(f"Failed to fetch data: HTTP {response.status}")
            return {}
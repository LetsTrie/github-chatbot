import os
import aiohttp
import logging
from GithubUrlManager import GithubUrlManager

async def fetch_github_count(endpoint, params=None):
    github_url_manager = GithubUrlManager()
    metadata = github_url_manager.get_metadata()
    
    url = f"https://api.github.com/repos/{metadata.get('owner')}/{metadata.get('repo')}/{endpoint}"

    headers = {
        "Authorization": f"Bearer {os.environ.get("GITHUB_ACCESS_TOKEN")}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    if params is None:
        params = {}

    params.update({"per_page": 1})

    logging.info(f"Fetching count from {url} with params: {params}")

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status != 200:
                logging.error(f"Failed to fetch count: HTTP {response.status}")
                logging.error(f"Response text: {await response.text()}")
                return None

            if "Link" in response.headers:
                links = response.headers["Link"].split(",")
                for link in links:
                    if 'rel="last"' in link:
                        last_url = link.split(";")[0].strip()[1:-1]
                        last_page = last_url.split("page=")[-1]
                        return int(last_page)

            return len(await response.json())
            
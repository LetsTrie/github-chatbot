import os
import aiohttp
import logging
from GithubUrlManager import GithubUrlManager

async def fetch_github_data(endpoint, params=None):
    github_url_manager = GithubUrlManager()
    metadata = github_url_manager.get_metadata()
    
    url = f"https://api.github.com/repos/{metadata['owner']}/{metadata['repo']}/{endpoint}"
    
    headers = {
        "Authorization": f"Bearer {os.environ.get("GITHUB_ACCESS_TOKEN")}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    per_page = params.get("per_page", 10) if params else 10

    if params is None:
        params = {}

    params.update({"per_page": per_page})

    logging.info(f"Fetching data from {url} with params: {params}")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status != 200:
                logging.error(f"Failed to fetch data: HTTP {response.status}")
                logging.error(f"Response text: {await response.text()}")
                logging.error(f"headers: {headers}")
                return None

            try:
                response_json = await response.json()

                if not response_json:
                    logging.info("No data found")
                    return []

                logging.info(f"Total data fetched: {len(response_json)} items")
                return response_json

            except aiohttp.ClientResponseError as e:
                logging.error("Failed to parse JSON response")
                logging.exception(e)
                return None

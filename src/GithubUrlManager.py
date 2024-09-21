import logging
from urllib.parse import urlparse

class GithubUrlManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GithubUrlManager, cls).__new__(cls)
            cls._instance.github_url = None 
        return cls._instance

    def set_url(self, url_value):
        self.github_url = url_value

    def get_url(self):
        return self.github_url

    def get_owner_and_repo(self):
        if not self.github_url:
            logging.error("GitHub URL is not set")
            return None, None
        
        parsed_url = urlparse(self.github_url)
        path_parts = parsed_url.path.strip('/').split('/')

        if len(path_parts) >= 2:
            return path_parts[0], path_parts[1]
        
        logging.error("Invalid GitHub URL")
        return None, None

    def get_metadata(self):
        owner, repo = self.get_owner_and_repo()
        return {"owner": owner, "repo": repo} if owner and repo else None
import os
import asyncio
from agent import Agent
from helpers.chat import chat
from GithubAgent import GitHubAgent
from dotenv import load_dotenv, find_dotenv
from utils.setup_logger import setup_logger
from GithubUrlManager import GithubUrlManager

load_dotenv(find_dotenv())

setup_logger(os.getenv('ENVIRONMENT', 'dev'))

if __name__ == "__main__":
    # git_url = input("Please provide a github repository URL: ")
    git_url = "https://github.com/freeCodeCamp/freeCodeCamp"
    
    github_url_manager = GithubUrlManager()
    github_url_manager.set_url(git_url)
    
    github_agent = GitHubAgent(git_url)
    github_agent_prompt = github_agent.create_prompt()
    
    query = Agent(github_agent_prompt)
    
    asyncio.run(chat(query))
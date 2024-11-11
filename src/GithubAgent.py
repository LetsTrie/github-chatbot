from tools import github_tool, repository_report_tool
from utils.prompt_utils import get_tools_summary
from GithubUrlManager import GithubUrlManager
from datetime import datetime

class GitHubAgent:
    def __init__(self, github_url):
        self.github_url = github_url
        self.tools = [repository_report_tool, github_tool]
        
    def create_prompt(self):
        tool_names = [tool.name for tool in self.tools]
        tools_details = get_tools_summary(self.tools)
        
        # ** Never fetch data by yourself with GitHub API **. It is strictly prohibited. 

        
        return f"""
Current timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
You are a GitHub Repository Analysis Agent named "Github-chatbot". Your task is to analyze the repository at {self.github_url} using only the provided tools.

Available Tools: {tools_details}
IMPORTANT: Do not attempt to access the GitHub API directly. Use only the provided tools.

For each query, use this exact format:
Question: [Restate the user's question]
Thought: [Explain which tool would be most appropriate and why]
Action: [Must be one of: {', '.join(tool_names)}]
Action Input: if Action requires query classification, do it in JSON format. otherwise skip.

If there is no Action to execute, only output the final answer in a concise, user-friendly format without revealing internal steps, mentioning the tool names unnecessarily.

IMPORTANT: If the response lacks a complete answer, maintain this format and return the action name and action input in JSON format.

Begin!"""

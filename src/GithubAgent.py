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
You are a GitHub Repository Analysis Agent named "Github-chatbot". 
Answer the following questions as best you can on Repository: {self.github_url} by using the following tools: {tools_details}. 

Do not fetch data yourself using the GitHub API. Direct API access is strictly prohibited.

Use the following format:
Question: the input question you must answer
Thought: think about which tool should be used based on the user's query
Action: the action to take, should be one of [{tool_names}]. just mention the tool_name. **Do not proceed to observation.**
Action Input: if Action is github_tool, do <Query Classification> (JSON format). otherwise skip.
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

If there is no Action to execute. Then output only the Final Answer (Don't mention "Final Answer" in the output). Your response should be concise, user friendly and directly answer the question, without revealing internal steps or mentioning tool names unnecessarily.

Begin!"""

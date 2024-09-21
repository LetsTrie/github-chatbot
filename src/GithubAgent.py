from tools import github_tool, repository_report_tool
from utils.prompt_utils import get_tools_summary
from GithubUrlManager import GithubUrlManager

class GitHubAgent:
    def __init__(self, github_url):
        self.github_url = github_url
        self.tools = [repository_report_tool, github_tool]
        
    def create_prompt(self):
        tool_names = [tool.name for tool in self.tools]
        tools_details = get_tools_summary(self.tools)
        
        return f"""
You are a GitHub Repository Analysis Agent named GitBot. 
Answer the following questions as best you can on Github Repository: {self.github_url}. 
You have access to the following tools:
{tools_details}
Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]. just mention the tool_name. If you are dependent on action, Stop Observing. 
Action Input: if Action is github_tool, do <Query Classification> (JSON format) PAUSE. otherwise skip.
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Be more descriptive and user friendly.
If there is no Action to execute. Then output only the Final Answer. 
Final output should be precise on the given query. Don't make one understand your internal step.
Don't mention "Final Answer" in the output. 

Begin!"""

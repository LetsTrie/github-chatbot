from enum import Enum
from typing import Optional
from langchain.tools import tool
from langchain.tools.base import StructuredTool
from langchain.pydantic_v1 import BaseModel, Field
from helpers.core import get_count, get_multiple_documents
from utils.datetime import format_since_datetime

class EndpointEnum(str, Enum):
    commits = "commits"
    pulls = "pulls"
    issues = "issues"

class ScopeEnum(str, Enum):
    count = "count"
    single_document = "single_document"
    multiple_documents = "multiple_documents"

class StateEnum(str, Enum):
    open = "open"
    closed = "closed"
    all = "all"

class GithubToolInput(BaseModel):
    endpoint: Optional[EndpointEnum] = Field(None, description="Type of action ('commits', 'pulls', 'issues').")
    scope: Optional[ScopeEnum] = Field(None, description="Scope of the query ('count', 'single_document', 'multiple_documents').")
    state: Optional[StateEnum] = Field(None, description="State of the pull requests/issues ('open', 'closed', 'all').")
    limit: Optional[int] = Field(None, description="Maximum number of items to retrieve.")
    since: Optional[str] = Field(None, description="Date range since format '{{number}}{{h/d/m/y}}' (e.g., '7d' for last 7 days).")
    author: Optional[str] = Field(None, description="Author's username to filter items.")

async def github_exec(args: GithubToolInput) -> dict:
    """
    This tool interacts with the GitHub API to retrieve various types of data from a repository. 
    It can fetch information about commits, pull requests, or issues, and can either count items, retrieve multiple items, or get details of a single item.
    (To use this tool, query must be classified as per the description of the function arguments.)
    """

    action = args.get("action")
    scope  = args.get("scope") 
    state  = args.get("state") 
    limit  = args.get("limit") 
    since  = args.get("since") 
    author  = args.get("author") 
    
    since = format_since_datetime(since)   
    per_page = min(10, int(limit)) if limit is not None else 10

    params = {}
    if isinstance(author, str):
        params["author"] = author
    if isinstance(state, str):
        params["state"] = state
    if isinstance(since, str):
        params["since"] = since

    if scope == "count":
        count = await get_count(action, params)
        return { "data": count }

    params["per_page"] = per_page

    if scope == "multiple_documents":
        docs = await get_multiple_documents(action, params)
        return { "data": docs }

    return { "data": None }

github_tool = StructuredTool.from_function(
    func=github_exec,
    name="github_tool",
    args_schema=GithubToolInput,
    coroutine=github_exec
)
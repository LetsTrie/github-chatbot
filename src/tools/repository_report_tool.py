from langchain.tools.base import StructuredTool
from helpers.get_repository import get_repository

async def repository_report_exec() -> dict:
    """
    Fetch the repository report. Always show as a list in markdown and end with a summary.
    """
    repository = await get_repository()
    return {
        "data": repository
    }

repository_report_tool = StructuredTool.from_function(
    func=repository_report_exec,
    name="repository_report_tool",
    coroutine=repository_report_exec
)
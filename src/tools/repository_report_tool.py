from langchain.tools.base import StructuredTool
from helpers.get_repository import get_repository

async def repository_report_exec() -> dict:
    """
    This tool fetches general information about a GitHub repository, including metadata and statistics. It returns a report as a list in markdown format, ending with a summary. Use this for a broad overview of the repository.
    """
    print("Calling \"repository_report_tool.\"...")
    repository = await get_repository()
    return {
        "data": repository
    }

repository_report_tool = StructuredTool.from_function(
    func=repository_report_exec,
    name="repository_report_tool",
    coroutine=repository_report_exec
)
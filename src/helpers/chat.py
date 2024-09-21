import json
from tools import github_tool, repository_report_tool
from utils.parser_utils import parse_and_validate_output

async def chat(query):  
    while True:
        user_input = input("User: ")
    
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break
    
        next_prompt = user_input
        result = ""

        is_primary_query = True
        max_iteration = 5
        while max_iteration != 0:
            max_iteration -= 1
            
            result = query(next_prompt, is_primary_query)
            is_primary_query = False

            parser = parse_and_validate_output(result)
            
            if parser["action"] == "github_tool":
                data = await github_tool.coroutine({
                    "action" : parser.get("endpoint"), 
                    "scope"  : parser.get("scope"), 
                    "state" : parser.get("state"), 
                    "limit"  : parser.get("limit"), 
                    "since"  : parser.get("since"), 
                    "author" : parser.get("author")
                })
                next_prompt = json.dumps(data)
    
            elif parser["action"] == "repository_report_tool":
                data = await repository_report_tool.coroutine()
                next_prompt = json.dumps(data)
    
            else:
                break
    
        print("Git-Bot:", result)
        query.finalize()
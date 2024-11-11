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
        
        index = 1
        max_iteration = 5
        while max_iteration != 0:
            max_iteration -= 1
            if index != 1:
                print("\n")
                
            print("****************************************************")
            print(f"iteration: {index}")
            print("****************************************************")
            print(f"prompt: {next_prompt}")
            
            index += 1
            
            result = query(next_prompt, is_primary_query)
            print("\n>>>>> Model Response: >>>>>>>>>>>>>>>>>>>>>>>")
            print(result)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            is_primary_query = False

            parser = parse_and_validate_output(result)
            print("\n>>>>> Parser Response: >>>>>>>>>>>>>>>>>>>>>>>")
            print(parser)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
            
            if parser["action"] == "github_tool":
                data = await github_tool.coroutine({
                    "action" : parser.get("endpoint"), 
                    "scope"  : parser.get("scope"), 
                    "state" : parser.get("state"), 
                    "limit"  : parser.get("limit"), 
                    "since"  : parser.get("since"), 
                    "author" : parser.get("author"),
                    "until" : parser.get("until"),
                })
                next_prompt = json.dumps(data)
    
            elif parser["action"] == "repository_report_tool":
                data = await repository_report_tool.coroutine()
                next_prompt = json.dumps(data)
    
            else:
                break
            
        print("\n" + "="*40)
        print("|{:^38}|".format("FINAL ANSWER"))
        print("="*40)
        print(f"\n{result:^40}")
        print("="*40 + "\n")
        
        query.finalize()
# src/utils/parser_utils.py
import re
import json

def parse_and_validate_output(output_string):
    result = {
        "action": None,
        "endpoint": None,
        "scope": None,
        "state": None,
        "since": None,
        "limit": None,
        "author": None
    }

    if action_match := re.search(r"Action:\s*(\w+)", output_string):
        # print(action_match)
        result["action"] = action_match.group(1)

    action_input_match = re.search(
        r"Action Input:\s*({.*?})\s*(?:PAUSE)?", 
        output_string, 
        re.DOTALL
    )

    if action_input_match:
        try:
            json_string = action_input_match.group(1).strip()  
            action_input = json.loads(json_string)
            
            for key in result:
                if key in action_input:
                    value = action_input[key]
                    if value == "None":
                        result[key] = None
                    elif key == "limit" and value is not None:
                        result[key] = int(value)
                    else:
                        result[key] = value
                        
        except json.JSONDecodeError as e:
            print(f"Error: Unable to parse Action Input JSON: {str(e)}")

    return result

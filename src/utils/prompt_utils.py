from enum import Enum

def get_tools_summary(tools):
    details = "\n===========\n"
    for tool in tools:
        tool_args = tool.args_schema.__fields__.items()
        
        details += f"Tool Name: {tool.name}\n"
        details += f"Tool description: {tool.description}\n"
        details += f"Arguments:\n" if len(tool_args) > 0 else f"No Arguments\n"
        
        for field_name, field_info in tool_args:
            field_type = field_info.type_
            details += f" - {field_name}: {field_info}\n"
            details += f"   Description: {field_info}\n"
            
            if isinstance(field_type, type) and issubclass(field_type, Enum):
                enum_values = [e.name for e in field_type]
                details += f"   Enum values: {enum_values}\n"

        details += "===========\n"  

    return details

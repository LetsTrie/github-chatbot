from enum import Enum



def get_tools_summary(tools):
    details = "\n===========\n"
    for tool in tools:
        tool_args = tool.args_schema.__fields__.items()
        
        details += f"Tool Name: {tool.name}\n"
        details += f"Tool description: {tool.description}\n"
        details += f"Arguments:\n" if len(tool_args) > 0 else f"No Arguments\n"

# name='endpoint' type=Optional[EndpointEnum] required=False default=None
# Description: ....
# Enum values: ['commits', 'pulls', 'issues']

        for field_name, field_info in tool_args:
            field_annotation = field_info.annotation  
            field_required = field_info.is_required() 
            field_default = field_info.default  
            field_description = field_info.description  

            if isinstance(field_annotation, type) and issubclass(field_annotation, Enum):
                enum_values = [e.name for e in field_annotation]
                field_type = f"Optional[ENUM({', '.join(enum_values)})]"
            else:
                field_type = field_annotation

            details += f" - name='{field_name}' type={field_type} required={field_required} default={field_default}\n"
            details += f"   Description: {field_description}\n"
        
        details += "===========\n"  

    return details

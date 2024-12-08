FUNCTION_PROMPT_TEMPLATE = '''Apply the function below to the given input. The function will be worded in natural language.

You must return your response in the following form:
{response_format}

Function Name: {function_name}

Function Description:
{function_description}

Input:
{function_input}'''


RESPONSE_FORMAT_PROMPT_TEMPLATE = '''Give your answer in the form of a JSON object.
The object should have the following fields:
{{
    "output": ..., // The output of the function, in the format specified below. If there was an error in the function, return a detailed description of why.
    "error": ... // Optional boolean (NOT string). If there was an error in the function, this should be true. Otherwise, it should be false or omitted.
}}

Output Format:
{output_format}'''


OUTPUT_FORMATS = {
    str: "A string",
    int: "An integer",
    float: "A float"
}


def build_response_format(return_type: type):

    # Get natural language description of return type
    output_format_name = OUTPUT_FORMATS.get(return_type)
    if not output_format_name:
        raise ValueError("Invalid return type")
    
    # Generate response format string
    return RESPONSE_FORMAT_PROMPT_TEMPLATE.format(output_format=output_format_name)
    
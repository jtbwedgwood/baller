import inspect
import json

from functools import wraps

from errors import LLMError
from prompts import FUNCTION_PROMPT_TEMPLATE, build_response_format, OUTPUT_FORMATS
from utils import invoke_llm, trim_json


# Decorator to turn a function into an "LLM function"
def llm_function(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        
        # An error is raised if there is not just a single string passed in
        sig = inspect.signature(func)
        params = sig.parameters
        arg_types = {name: param.annotation for name, param in params.items()}
        if len(args) != 1 or len(arg_types) != 1:
            raise ValueError("Only one argument is allowed")
        if not isinstance(args[0], str) or list(arg_types.values())[0] is not str:
            raise ValueError("Function argument must be a string")
        
        # Generate response format string based on function return type
        return_type = sig.return_annotation
        if return_type not in OUTPUT_FORMATS.keys():
            raise ValueError(f"Function must return one of the following: {', '.join([str(rt) for rt in OUTPUT_FORMATS.keys()])}")
        response_format = build_response_format(return_type)

        # Get name, description, and input of function
        function_name = func.__name__
        function_description = func.__doc__
        function_input = args[0]

        # Generate prompt and invoke LLM
        prompt = FUNCTION_PROMPT_TEMPLATE.format(
            response_format=response_format,
            function_name=function_name,
            function_description=function_description,
            function_input=function_input
        )
        try:
            llm_response = invoke_llm(prompt)
        except Exception as e:
            raise LLMError("Error invoking LLM") from e
        
        # Extract response and convert to right type, then return
        llm_response = trim_json(llm_response)
        llm_response_json = json.loads(llm_response)
        if llm_response_json.get("error"):
            raise LLMError(f"Error in function: {llm_response_json['output']}")
        try:
            output = return_type(llm_response_json["output"])
            return output
        except ValueError as e:
            raise LLMError("LLM output could not be converted to correct type") from e
        
    return wrapper
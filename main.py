# to activate virtual environment: source .venv/bin/activate
# to run: uv run main.py

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.config import *
from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python_file import *
from functions.write_file import *

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    messages = [
        types.Content(role="user", parts=[types.Part(text=get_prompt())]),
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT),
    )

    function_calls = response.function_calls or []

    for function_call_part in function_calls:
        function_call_result = call_function(function_call_part)
        
        try:
            if not function_call_result.parts[0].function_response.response:
                raise Exception("call_function didnt return a correct response")    
            elif sys.argv[1] and sys.argv[2] == "--verbose":
                print(f"-> {function_call_result.parts[0].function_response.response}")
        except IndexError:
            pass

    if len(function_calls) == 0:
        print(response.text)
        
    verbose(response)



def get_prompt():
    return sys.argv[1]

def verbose(response):
    try:
        if sys.argv[1] and sys.argv[2] == "--verbose":
            print(f"User prompt: {get_prompt()}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    except IndexError:
        pass


def call_function(function_call_part, verbose=False):
    func_dict = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    
    if function_call_part.name in func_dict:

        raw_args = function_call_part.args

        if not raw_args:
            kwargs = {}
        elif isinstance(raw_args, dict):
            kwargs = raw_args.copy()
        else:
            try:
                kwargs = dict(raw_args)
            except Exception:
                kwargs = {}

        kwargs["working_directory"] = "./calculator"

        function_result = func_dict[function_call_part.name](**kwargs)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

if __name__ == "__main__":
    main()

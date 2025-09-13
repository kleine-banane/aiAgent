# to activate virtual environment: source .venv/bin/activate
# to run: uv run main.py

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.config import *
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

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

    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

    if len(response.function_calls) == 0:
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

if __name__ == "__main__":
    main()

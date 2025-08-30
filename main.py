# to activate virtual environment: source .venv/bin/activate
# to run: uv run main.py

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.config import *

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    messages = [
        types.Content(role="user", parts=[types.Part(text=get_prompt())]),
    ]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
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

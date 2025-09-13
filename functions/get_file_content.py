import os
from functions.config import *
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not target_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_path, "r") as f:
            file_content = f.read(MAX_CHARS)
            if len(file_content) == MAX_CHARS:
                return f'{file_content} \n [...File "{file_path}" truncated at 10000 characters]'

            return file_content
    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Gives content of the specified file. If the file contains more than {MAX_CHARS} characters, it will be truncated",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to get content from, relative to the working directory. Mandatory.",
            ),
        },
    ),
)
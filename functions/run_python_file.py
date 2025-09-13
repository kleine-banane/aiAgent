import os
import subprocess
from functions.config import *
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not target_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'
    if not target_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        command = ["uv", "run", target_path] + args
        process = subprocess.run(command, timeout=TIME_OUT, capture_output=True)

        if not process.stderr and not process.stdout:
            return "No output produced."

        std_string = f"STDOUT:\n{process.stdout.decode("utf-8")} \nSTDERR:\n{process.stderr.decode("utf-8")}"
        if process.returncode != 0:
            code_string = f"Process exited with code {process.returncode}"
        else:
            code_string = ""

        return f"{std_string}\n{code_string}"

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the specified python file in the working directory. If no args are provided, run without args.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Optional CLI args. If omitted, none are used."
            )
        },
    ),
)
    
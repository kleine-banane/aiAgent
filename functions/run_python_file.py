import os

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not target_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'
    if not target_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    
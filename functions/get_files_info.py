import os

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    
    target_path = os.path.abspath(os.path.join(working_directory, directory))
    
    if not target_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_path):
        return f'Error: "{directory}" is not a directory'


    try:
        contents = os.listdir(target_path)
        contents_list = []

        for item in contents:
            item_path = os.path.join(target_path, item)
            contents_list.append(f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")

        return "\n".join(contents_list)
    except Exception as e:
        return f"Error: {e}"
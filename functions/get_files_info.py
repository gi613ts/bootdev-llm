import os
from functions.config import project_path


def get_files_info(working_directory, directory="."):
    
    directory_abs = os.path.abspath(working_directory)
    requested_full_path = os.path.join(directory_abs, directory)
    clean_path = os.path.abspath(requested_full_path)

    if not clean_path.startswith(project_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(clean_path):
        return f'Error: "{directory}" is not a directory'

    try:
        report = ""
        contents = os.listdir(clean_path)
        for item in contents:
            try:
                report += f"- {item}: file_size={os.path.getsize(clean_path + "/" + item)} bytes, is_dir={os.path.isdir(clean_path + "/" + item)}\n"
            except Exception as error:
                print("Error: {error}")

        return report
    
    except Exception as e:
        return "Error getting file info: {e}"
    
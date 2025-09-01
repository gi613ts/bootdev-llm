import os
from functions.config import project_path


def write_file(working_directory, file_path, content):

    directory_abs = os.path.abspath(working_directory)
    requested_full_path = os.path.join(directory_abs, file_path)
    clean_path = os.path.abspath(requested_full_path)

    if not os.path.abspath(clean_path).startswith(project_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isdir(clean_path):
        return f'Error: Name of an existing directory given : "{clean_path}"'

    clean_path_dir = "/".join((clean_path.split("/")[:-1]))

    if not os.path.exists(clean_path_dir):
        try:
            os.makedirs(clean_path_dir)
        except Exception as e:
            return f'Error while creating path: {e}'
    
    try:
        with open(clean_path, "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error encountered when writing to file: {e}"
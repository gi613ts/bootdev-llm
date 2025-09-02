import os
from functions.config import project_path, max_file_length

def get_file_content(working_directory, file_path):
    
    directory_abs = os.path.abspath(working_directory)
    requested_full_path = os.path.join(directory_abs, file_path)
    clean_path = os.path.abspath(requested_full_path)

    if not clean_path.startswith(project_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'


    if os.path.isfile(clean_path) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'

    
    try:
        with open(clean_path, "r") as file:
            file_content_string = file.read(max_file_length)
            if os.path.getsize(clean_path) > 10000:
                file_content_string += f'...File "{file_path}" truncated at 10000 characters'
            return file_content_string
    except Exception as e:
        return f"Error encountered when opening file: {e}"




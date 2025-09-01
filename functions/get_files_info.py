import os

project_path = "/home/unix/github/gi613ts/bootdev-llm/calculator"

def get_files_info(working_directory, directory="."):
    
    directory_abs = os.path.abspath(working_directory)
    requested_full_path = os.path.join(directory_abs, directory)

    if os.path.isdir(requested_full_path) == False:
        return f'Error: "{directory}" is not a directory'

    if (os.path.abspath(requested_full_path)).startswith(project_path):
        report = ""
        contents = os.listdir(requested_full_path)
        for item in contents:
            try:
                report += f"- {item}: file_size={os.path.getsize(requested_full_path + "/" + item)} bytes, is_dir={os.path.isdir(requested_full_path + "/" + item)}\n"
            except Exception as error:
                print("Error: {error}")

        return report
    else:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    

def get_file_content(working_directory, file_path):
    
    directory_abs = os.path.abspath(working_directory)
    requested_full_path = os.path.join(directory_abs, file_path)

    

    if os.path.isfile(requested_full_path) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'

    
    if (os.path.abspath(requested_full_path)).startswith(project_path):
        print("good file")
    else:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
import os
import subprocess
from functions.config import project_path


def run_python_file(working_directory, file_path, args=[]):

    directory_abs = os.path.abspath(working_directory)
    requested_full_path = os.path.join(directory_abs, file_path)
    clean_path = os.path.abspath(requested_full_path)

    if not os.path.abspath(clean_path).startswith(project_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(clean_path):
        return f'Error: File "{file_path}" not found.'
    
    if clean_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    call = ["uv", "run", clean_path]
    call.extend(args)
    
    try:
        script_result = subprocess.run(call, capture_output=True, timeout=30, text=True)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    output = ""
        

    output += f"STDOUT: \n{script_result.stdout}\n"

    output += f"STDERR: \n{script_result.stderr}\n"

    if script_result.returncode != 0:
        output += f"Process exited with code {script_result.returncode}"


    if script_result.stdout == "":
        output += "\nNo output produced.\n"
    
    return output

    

    


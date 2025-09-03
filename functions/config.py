from google import genai
from google.genai import types

project_path = "/home/unix/github/gi613ts/bootdev-llm/calculator"
max_file_length = 10000

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the contents of a file in the specified directory as text, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file which contents are to be returned, relative to the working directory."
            ),
        },
    ),
)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes specified contents to a file specified by a given path, relative to the working directory. If a file doesn't exist, it's created. Constrained to the working directory.",
    parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file path to the file which contents are to be overwritten, relative to the working directory."
                
            ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to be written to the specified file."
            ),
         },
        
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified python script with given arguments. Restricted to the working directory.",
    parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file path to the python file to be executed, relative to the working directory."
                
            ),
                "args": types.Schema(
                    type=types.Type.STRING,
                    description="List of arguments to pass to the called function. Defaults to an empty list."
                
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Overwrite the contents of a file
- Run a python file with arguments

Do not ask the user for information you can get by performing these operations.

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
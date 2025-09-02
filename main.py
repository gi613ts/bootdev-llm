import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.config import *
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python import run_python_file

def main():

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("this script takes one argument (the prompt string) and an optional --verbose switch")
        sys.exit(1)
    
    verbose = "--verbose" in sys.argv

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    prompt = sys.argv[1]

    if verbose:
        print(f"User prompt: {prompt}")

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    generate_content(client, messages, verbose)




def generate_content(client, messages, verbose):

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
        )
    )
    
    if verbose:
        usage_numbers = response.usage_metadata
        print(f"Prompt tokens: {usage_numbers.prompt_token_count}")
        print(f"Response tokens: {usage_numbers.candidates_token_count}")

    if not response.function_calls:
        return response.text

    function_results = []
    for function_call in response.function_calls:
        function_result = call_function(function_call, verbose)
        if (
            not function_result.parts or
            not function_result.parts[0].function_response
        ):
            raise Exception("Function call failed, function_result object is None")
        if verbose:
            print(f"-> {function_result.parts[0].function_response.response}")
        function_results.append(function_result.parts[0])
        print(function_results)
    
    if function_results == []:
        raise Exception("Function result list is empty")


    """
    for response in response.candidates:
        messages.append(response)

    #print("response candidates: ", response.candidates)
    #print("response candidate item: ", response.candidates[0])
    #print("response candidate item content: ", response.candidates[0].content)

    print("call output: ", call_output)
    print("messages: ", messages)

    """







def call_function(function_call_part, verbose=False):

    functions_dict = {"get_files_info":get_files_info, 
                      "get_file_content":get_file_content,
                      "write_file":write_file,
                      "run_python_file":run_python_file}
    
    if function_call_part.name not in functions_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    function_name = function_call_part.name
    function_run = functions_dict[function_name]
    
    function_args = {"working_directory":project_path}
    function_args.update(function_call_part.args)

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function_result = function_run(**function_args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )

    

if __name__ == "__main__":
    main()

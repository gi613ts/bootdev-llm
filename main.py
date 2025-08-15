import os
import sys
from dotenv import load_dotenv
from google import genai



def main():

    if len(sys.argv) != 2:
        print("this script takes one argument (the prompt string)")
        sys.exit(1)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    prompt = sys.argv[1]

    response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=prompt
    )

    print(response.text)

    usage_numbers = response.usage_metadata
    print(f"Prompt tokens: {usage_numbers.prompt_token_count}")
    print(f"Response tokens: {usage_numbers.candidates_token_count}")

if __name__ == "__main__":
    main()

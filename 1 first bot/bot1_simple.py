
# pip install google-genai
# pip install python-dotenv

from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
load_dotenv('keys.env')  # Load environment variables from .env file
api_key = os.getenv('GOOGLE_API_KEY')

client = genai.Client(api_key=api_key)
chat = client.chats.create(model='gemini-2.0-flash-lite')

### The chat assistance starts here
print("Type your prompts (type 'exit' to quit):")
try:
    while True:
        prompt = input("> ")
        if prompt.lower() == 'exit':
            break
        ## Show full response once generated
        # response = chat.send_message(prompt)
        # print(response.text)

        ## Show response in streaming mode
        for chunk in client.models.generate_content_stream(
            model='gemini-2.0-flash',
            contents=prompt,):
            print(chunk.text)
        print()  # New line after response

except KeyboardInterrupt:
    print("\nExiting chat.")







# def main():
#     api_key = os.getenv('GOOGLE_API_KEY')
#     if not api_key:
#         raise EnvironmentError("GOOGLE_API_KEY environment variable not set.")
#     # genai.configure(api_key=api_key)
#     client = genai.Client(api_key=api_key)

#     # List available models
#     available_models = client.models.list()

#     print("Available models:")
#     # for model in available_models:
#     #     if 'generateContent' in model.supported_generation_methods:
#     #         print(f"- {model.name}")
    
#     model_name = 'gemini-2.0-flash-lite'  # Update if needed after checking available models
#     # model = GenerativeModel(model_name)
#     # chat = model.start_chat(history=[])

#     print("Type your prompts (type 'exit' to quit):")
#     try:
#         while True:
#             prompt = input("> ")
#             if prompt.lower() == 'exit':
#                 break

#             response_stream = chat.send_message(prompt, stream=True)
#             for chunk in response_stream:
#                 if chunk.text:
#                     print(chunk.text, end='', flush=True)
#             print()  # New line after response

#     except KeyboardInterrupt:
#         print("\nExiting chat.")

# if __name__ == "__main__":
#     main()

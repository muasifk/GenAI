

# pip install google-genai
# pip install python-dotenv

from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
from google.genai.types import ModelContent, Part, UserContent
load_dotenv('../keys.env')  # Load environment variables from .env file
api_key = os.getenv('GOOGLE_API_KEY')


##############################################################
# The chat assistance using "chat" method
##############################################################
client = genai.Client(api_key=api_key)
chat = client.chats.create(model='gemini-2.0-flash-lite',
                           history=[
                               UserContent(parts=[Part(text="Hello")]),
                                ModelContent(
                                    parts=[Part(text="Great to meet you. What would you like to know?")],
                                ),
                            ],
                            )

### The chat assistance starts here
print("Type your prompts (type 'exit' to quit):")
try:
    while True:
        prompt = input("[User:] > ")
        if prompt.lower() == 'exit':
            break
        ## Show full response once generated
        response = chat.send_message(prompt)
        print("[Assistant:] > ", response.text)
        print()  # New line after response

except KeyboardInterrupt:
    print("\nExiting chat.")








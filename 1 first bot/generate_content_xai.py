

# pip install google-genai
# pip install python-dotenv

from dotenv import load_dotenv
import os
from openai import OpenAI
from google.genai import types
load_dotenv('keys.env')  # Load environment variables from .env file
api_key = os.getenv('XAI_API_KEY2')
client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1",)  


response = client.chat.completions.create(
  model="grok-3",
  messages=[
    {"role": "user", 
     "content": "Tell me a story of a titans in at least 50 lines."}
  ]
)

os.system('cls' if os.name == 'nt' else 'clear')
print(response.text)
# print(response.model_dump_json(exclude_none=True, indent=4))






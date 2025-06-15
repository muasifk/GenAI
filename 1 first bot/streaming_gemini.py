

# pip install google-genai
# pip install python-dotenv

from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
load_dotenv('keys.env')  # Load environment variables from .env file
api_key = os.getenv('GOOGLE_API_KEY')
  


client = genai.Client(api_key=api_key)
for chunk in client.models.generate_content_stream(
  model='gemini-2.0-flash',
  contents='Tell me a story in 300 words.'
):
    print(chunk.text)





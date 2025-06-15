

# pip install google-genai
# pip install python-dotenv

from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
load_dotenv('keys.env')  # Load environment variables from .env file
api_key = os.getenv('GOOGLE_API_KEY')
  


client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='Tell me a story of a titans in at least 50 lines.',
    config=types.GenerateContentConfig(
      system_instruction='you are a story teller with a good common sense',
      max_output_tokens= 5000,
      # top_k= 2,
      # top_p= 0.5,
      temperature= 0.9,
    #   response_mime_type= 'application/json',
      stop_sequences= ['\n'],
      seed=42,
      safety_settings= [types.SafetySetting(
              category='HARM_CATEGORY_HATE_SPEECH',
              threshold='BLOCK_ONLY_HIGH'),]
    ),
)

os.system('cls' if os.name == 'nt' else 'clear')
print(response.text)
# print(response.model_dump_json(exclude_none=True, indent=4))






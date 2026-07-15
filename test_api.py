from google import genai
from dotenv import load_dotenv
import os

# load enviroment variables from .env file
load_dotenv()

# create the OpenAI client using the API key from .env
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# send a simple text message and get a response
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Say hello and confirm you are working, in one short sentence."
)

# print the AI's reply
print(response.text)

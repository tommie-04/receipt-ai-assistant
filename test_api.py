from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

# load enviroment variables from .env file
load_dotenv()

# create the OpenAI client using the API key from .env
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# read the receipt image as raw bytes
with open("test_receipt.png", "rb") as f:
    image_bytes = f.read()

# send the image and instruction to Gemini
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
        "Extract the merchat name, total amount, and data from this receipt. Return the result as JSON with keys: merchant, total, date."
    ]
)

# print the AI's reply
print(response.text)

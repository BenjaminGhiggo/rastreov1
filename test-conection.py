import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found in .env file")

genai.configure(api_key=api_key)

prompt = "Escribe un poema sobre la naturaleza."
model_name = "models/gemini-1.5-flash"
response = genai.GenerativeModel(model_name).generate_content(prompt)
print(response.text.strip())

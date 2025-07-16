import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the API key from .env file
load_dotenv()

# Configure the Gemini SDK
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# List available models and their supported methods
for model in genai.list_models():
    print(model.name, model.supported_generation_methods)

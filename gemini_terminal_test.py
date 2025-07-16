import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Correct configuration
genai.configure(api_key=os.getenv("AIzaSyBj9mwWH2K4HOt_g98ZI-VTRkl41e_iLnU"))

# Use Gemini Pro — text only model (no images)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

prompt = input("Ask Gemini something: ")

try:
    response = model.generate_content(prompt)
    print("\nGemini says:\n", response.text)
except Exception as e:
    print("Error:", e)

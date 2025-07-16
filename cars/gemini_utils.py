import os
import google.generativeai as genai

# Optional: load environment variable (use python-dotenv or set manually)
genai.configure(api_key=os.getenv("AIzaSyBj9mwWH2K4HOt_g98ZI-VTRkl41e_iLnU"))

def get_ocean_fact():
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content("Give me a fun fact about the ocean.")
    return response.text

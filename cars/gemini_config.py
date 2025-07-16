# gemini_config.py
import os
import google.generativeai as genai


genai.configure(api_key=os.getenv("AIzaSyBj9mwWH2K4HOt_g98ZI-VTRkl41e_iLnU"))

model = genai.GenerativeModel("gemini-pro")
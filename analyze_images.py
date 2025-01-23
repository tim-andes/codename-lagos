# import os
import sys
# import re
import base64
# import httpx 
# import pathlib
from PIL import Image

import google.generativeai as genai
import google.generativeai.types.safety_types as safetype

system_prompt = """

You are an Unidentified Aerial Phenomena and Nonhuman Intelligence researcher. 
Your job is to analyze documents containing text, images, tables, and redacted 
information and find trends, patterns, outliers, and make connections between
documents and your general knowledge.

"""
class Query:
        def __init__(self):
            """
            """
            genai.configure(api_key="AIzaSyA5nKFXdBRr6A4unM9v7NGbJEGMr2sa8Qc")

        def multiple_image_prompt(self, query):
            model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                system_instruction=system_prompt,
                safety_settings=safetype.LooseSafetySettingDict())
   
            image_path_1 = "../../pdf-fbi-scrape/image_output/page_1.jpg"  # Replace with the actual path to your first image
            image_path_2 = "../../pdf-fbi-scrape/image_output/page_2.jpg" # Replace with the actual path to your second image

            image_file_1 = Image.open(image_path_1)
            image_file_2 = Image.open(image_path_2)
            
            response = model.generate_content([system_prompt, image_file_1, image_file_2])

            print(response.text)           

            return response
        
if __name__ == "__main__":
        
        obj = Query()
        obj.multiple_image_prompt(" ".join(sys.argv[1:]))

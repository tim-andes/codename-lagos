import google.generativeai as genai
import google.generativeai.types.safety_types as safetype
import pdf_to_image
from PIL import Image
from PyPDF2 import PdfReader
import re

class Query:
        def __init__(self):
            """
            """
            try:
                with open("config.ini", "r") as f:
                    key = f.read().strip() 
            except FileNotFoundError:
                raise FileNotFoundError("config.ini file not found. Please create this file and add your API key.")

            genai.configure(api_key=key)

        def multiple_doc_prompt(self, query, doc_paths):
            model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                system_instruction=query,
                safety_settings=safetype.LooseSafetySettingDict())
            
            docs = []
            match_pdf = r"(?i)pdf"
            # match_image = r"(?i)jpg|jpeg|png"

            print("Pre-conversion: ", doc_paths)
            if re.search(match_pdf, str(doc_paths[0])):
                doc_paths = pdf_to_image.convert_pdf_to_images(doc_paths, "./images", format="jpg")    
                print("Post-pdf-conversion: ", doc_paths)

                for doc_path in doc_paths:
                    docs.append(doc_path)
                    response = model.generate_content([query, *docs])
                    print(response.text)           

                return response.text
            
            for doc_path in doc_paths:
                doc_path = Image.open(doc_path)
                docs.append(doc_path)
            
                response = model.generate_content([query, *docs])
                print(response.text)           

                return response.text

if __name__ == "__main__":
        
        obj = Query()
        obj.multiple_doc_prompt()

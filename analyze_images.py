from PIL import Image
import google.generativeai as genai
import google.generativeai.types.safety_types as safetype

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

        def multiple_image_prompt(self, query, image_paths):
            model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                system_instruction=query,
                safety_settings=safetype.LooseSafetySettingDict())
            
            images = []

            for image_path in image_paths:
                print(type(image_path))
                image = Image.open(image_path)
                print(type(image))
                images.append(image)
               
            response = model.generate_content([query, *images])

            # print(response.text)           

            return response.text
        
if __name__ == "__main__":
        
        obj = Query()
        obj.multiple_image_prompt()

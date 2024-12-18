import io
import base64
from ollama import chat
from PIL import Image

def image_base64_encoder(image_name):
    """
    This function takes in a string that represent the path to the image that has been uploaded by the user and the function
    is used to encode the image to base64. The base64 string is then returned.
    :param image_name: This is the path to the image file that the user has uploaded.
    :return: A base64 string of the image that was uploaded.
    """
    # opening the image file that was uploaded by the user
    open_image = Image.open(image_name)
    # creating a BytesIO object to store the image in memory
    image_bytes = io.BytesIO()
    # saving the image to the BytesIO object
    open_image.save(image_bytes, format=open_image.format)
    # converting the BytesIO object to a base64 string and returning it
    image_bytes = image_bytes.getvalue()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    # getting the appropriate file type as claude 3 expects the file type to be presented
    # file_type = f"image/{open_image.format.lower()}"
    # returning the base64 encoded image
    return image_base64

def analyze_image(image_name, text):
    system_prompt = """Describe every detail you can about this document, be extremely thorough and detail even the most minute aspects of the document. 
    
    If a more specific question is presented by the user, make sure to prioritize that answer.
    """
    # checking if the user inserted any text along with the image, if not, we set text to a default since claude expects
    # text in the text block of the prompt.
    if text == "":
        text = system_prompt

    # this is the primary prompt passed into Ollama moondream with the system prompt, user uploaded image in base64 and any
    # text the user inserted
    response = chat(
        model='moondream',
        messages=[{
            'role': 'user',
            'content': text,
            'images': [image_name],
        }],
    )
    print(response)
    return response
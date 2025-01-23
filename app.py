import analyze_images
from pathlib import Path
import os
import streamlit as st
import sys

system_prompt = """

You are an Unidentified Aerial Phenomena and Nonhuman Intelligence researcher. 
Your job is to analyze documents containing text, images, tables, and redacted 
information and find trends, patterns, outliers, and make connections between
documents and your general knowledge.

"""

# title of the streamlit app
st.title(f""":rainbow[Codename: Lagos. Document analysis research assistant.]""")
# directions on what can be done with this streamlit app
st.header(f"""Directions to use this application:
1. Upload a PDF (currently requires PDF to JPG conversion) and click the "Analyze Document" button.
2. Optionally, input a JSON spec to control image analysis prompt and return to specific attributes

""", divider='rainbow')
# default container that houses the document upload field
with st.container():
    # header that is shown on the web UI
    st.subheader('Document File Upload:')
    # document upload field, the specific ui element that allows you to upload the document
    # when document is uploaded it saves the file(s) to the directory, and creates a path to the document
    image_list = st.file_uploader('Upload document', type=["png", "jpg", "jpeg"], key="new", accept_multiple_files=True)
    # this is the text area that allows you to insert a custom JSON spec to contrdocument analysis
    # text_area = st.text_area("(optional) Insert extra request details here.")
    # this is the text that is shown on the front end, and is used as a default prompt
    # text = f"Analyze this document in extreme detail. Please return a JSON response with the most relevant details of the document. If present, use this example JSON to categorize the document{text_area}"
    # this is the button that triggers the invocation of the model, processing of tdocument and/or question
    result = st.button("Analyze Document(s)")
    # if the button is pressed, the model is invoked, and the results are output to the front end
    if result:
        # if document is uploaded, a file will be present, triggering document_to_text function
        if image_list is not None:
            image_paths = []
            # document is displayed to the front end for the user to see
            st.image(image_list[0])
            # determine the path to temporarily save the image file that was uploaded
            save_folder = "./images"
            # create a posix path of save_folder and the file names
            for image in image_list:
                save_path = Path(save_folder, image.name)
                image_paths.append(save_path)
                # write the uploaded image files to the save_folder specified above
                with open(save_path, mode='wb') as w:
                        w.write(image.getvalue())

                # once the save path exists...
                if save_path.exists():
                    # write a success message saying the image has been successfully saved
                    st.success(f'Image successfully saved!')
            # running the image to text task, and outputting the results to the front end
            obj = analyze_images.Query()
            response = obj.multiple_image_prompt(system_prompt, image_paths)

            st.write(response)
            
            # removing the image file that was temporarily saved to perform the question and answer task
            for save_path in image_paths:
                os.remove(save_path)


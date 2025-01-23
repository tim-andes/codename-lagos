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
st.title(f"""Codename: Lagos.
A document analysis research assistant.
""")
# directions on what can be done with this streamlit app
st.header(f"""How to Use:
1. Upload any number of declassified documents (currently requires JPG, PDF capability coming soon).
2. Click the "Analyze Document(s)" button.

""")
# default container that houses the document upload field
with st.container():
    # header that is shown on the web UI
    st.subheader('Document File Upload:')
    # document upload field, the specific ui element that allows you to upload the document
    # when document is uploaded it saves the file(s) to the directory, and creates a path to the document
    image_list = st.file_uploader('Upload document', type=["png", "jpg", "jpeg"], key="new", accept_multiple_files=True)
    # this is the text area that allows you to insert a custom JSON spec to contrdocument analysis
    # text_area = st.text_area("(optional) Insert extra request details here.")

    # this is the button that triggers the invocation of the model; processing of one or many images
    result = st.button("Analyze Document(s)")
    # if the button is pressed, the model is invoked, and the results are output to the front end
    if result:
        # if document is uploaded, a file will be present, triggering document_to_text function
        if image_list is not None:
            image_paths = []
            # document is displayed to the front end for the user to see
            st.image(image_list[0], width=400)
            # determine the path to temporarily save the image file that was uploaded
            save_folder = "./images"
            # create a posix path of save_folder and the file names
            for image in image_list:
                save_path = Path(save_folder, image.name)
                image_paths.append(save_path)
                # write the uploaded image files to the save_folder specified above
                with open(save_path, mode='wb') as w:
                        w.write(image.getvalue())

            # once the save paths exist...
            if image_paths[0].exists():
                    # write a success message saying the image has been successfully saved
                    st.success(f'Images received. Processing...')
            # running the image to text task, and outputting the results to the front end
            obj = analyze_images.Query()
            response = obj.multiple_image_prompt(system_prompt, image_paths)

            st.write(response)
            
            # removing the image file that was temporarily saved to perform the question and answer task
            for save_path in image_paths:
                os.remove(save_path)


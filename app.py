import analyze_images
from pathlib import Path
import os
import streamlit as st
import sys

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
    # when document is uploaded it saves the file to the directory, and creates a path to the document
    File = st.file_uploader('Upload document', type=["png", "jpg", "jpeg"], key="new")
    # this is the text area that allows you to insert a custom JSON spec to contrdocument analysis
    # text_area = st.text_area("(optional) Insert extra request details here.")
    # this is the text that is shown on the front end, and is used as a default prompt
    # text = f"Analyze this document in extreme detail. Please return a JSON response with the most relevant details of the document. If present, use this example JSON to categorize the document{text_area}"
    # this is the button that triggers the invocation of the model, processing of tdocument and/or question
    result = st.button("Analyze Document(s)")
    # if the button is pressed, the model is invoked, and the results are output to the front end
    if result:
        # if document is uploaded, a file will be present, triggering tdocument_to_text function
        if File is not None:
            # document is displayed to the front end for the user to see
            st.image(File)
            # determine the path to temporarily save the image file that was uploaded
            save_folder = "./images"
            # create a posix path of save_folder and the file name
            save_path = Path(save_folder, File.name)
            # write the uploaded image file to the save_folder you specified
            with open(save_path, mode='wb') as w:
                w.write(File.getvalue())
            # once the save path exists...
            if save_path.exists():
                # write a success message saying the image has been successfully saved
                st.success(f'Image {File.name} is successfully saved!')
                # running the image to text task, and outputting the results to the front end
                obj = analyze_images.Query()
                response = obj.multiple_image_prompt(" ".join(sys.argv[1:]))
                st.write(response.text)
                
                # removing the image file that was temporarily saved to perform the question and answer task
                os.remove(save_path)


import pdf2image
import os
from tkinter import filedialog

def create_output_path(filename, format):
    return f"{filename}.{format}"

def convert_pdf_to_images(pdf_files, output_dir, format="jpg"):
    pages_list = []
    for pdf_file in pdf_files: # Iterate over the list of files

            try: #handles errors for individual files
                pages = pdf2image.convert_from_path(pdf_file)

                for i, page in enumerate(pages):
                    output_filename = create_output_path(f"{os.path.splitext(os.path.basename(pdf_file))[0]}_page_{i+1}", format) #includes original file name
                    page.save(os.path.join(output_dir, output_filename))
                    pages_list.append(page)
                print(f"Converted {pdf_file}") #prints which file was converted
            except Exception as e:
                print(f"Error converting {pdf_file}: {e}") #prints specific error for file
    return pages_list

def select_pdf_and_directory():

    pdf_file_path = filedialog.askopenfilenames(
        title="Select a Document (PDF)...",
        filetypes=[('PDF Files', '*.pdf')]
    )

    if pdf_file_path:
        output_dir = filedialog.askdirectory(
            title="Select your output folder..."
        )
    else:
        print("You need to select a file to convert. Try again.")

    if pdf_file_path and output_dir:
        convert_pdf_to_images(pdf_file_path, output_dir)
        print(f"PDF to Image Conversion Complete. Saved to {output_dir}")
    else:
        print("Please select both a PDF file and an output directory.")

def main():
    select_pdf_and_directory()

if __name__ == "__main__":
    main()
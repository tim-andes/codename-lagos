from PIL import Image
import pdf2image
import os
import tkinter as tk
from tkinter import filedialog

def create_output_path(filename, format):
    return f"{filename}.{format}"

def convert_pdf_to_images(pdf_file, output_dir, format="jpg"):
    pages = pdf2image.convert_from_path(pdf_file)

    for i, page in enumerate(pages):
        output_filename = create_output_path(f"page_{i+1}", format)
        page.save(os.path.join(output_dir, output_filename))

def select_pdf_and_directory():
    pdf_file_path = filedialog.askopenfilename(
        title="Select a Document (PDF)...",
        filetypes=[('PDF Files', '*.pdf')]
    )

    output_dir = filedialog.askdirectory(
        title="Select your output folder..."
    )

    if pdf_file_path and output_dir:
        convert_pdf_to_images(pdf_file_path, output_dir)
        print(f"PDF to Image Conversion Complete. Saved to {output_dir}")
    else:
        print("Please select both a PDF file and an output directory.")


if __name__ == "__main__":
  select_pdf_and_directory()
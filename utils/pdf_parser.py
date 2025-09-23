import fitz  # PyMuPDF
from typing import IO

def extract_text_from_pdf(pdf_file: IO[bytes]) -> str:
    """
    Extracts text content from a given PDF file stream.

    Args:
        pdf_file: A file-like object opened in binary read mode.

    Returns:
        A string containing the extracted text from the PDF.
    """
    try:
        # Open the PDF file from the in-memory bytes
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        
        full_text = ""
        # Iterate through each page and extract text
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            full_text += page.get_text()
            
        return full_text
    except Exception as e:
        print(f"Error processing PDF file: {e}")
        return "Error: Could not extract text from the provided PDF."


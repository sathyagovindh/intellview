from io import BytesIO
from PyPDF2 import PdfReader  # Assuming you're using PyPDF2 to read PDF files


def extract_text_from_pdf(pdf_file):
    # Read the file content from FileStorage
    pdf_data = pdf_file.read()  # This reads the file as bytes

    # Use BytesIO to convert bytes into a file-like object
    pdf_file_obj = BytesIO(pdf_data)

    # Now, extract text from the PDF file-like object
    pdf_reader = PdfReader(pdf_file_obj)
    text = ''

    # Iterate through the pages and extract text
    for page in pdf_reader.pages:
        text += page.extract_text()

    return text

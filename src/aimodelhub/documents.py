import os
from docx import Document
import fitz


def extract_from_pdf(file_path, max_pages=None):
    """
    Extracts text from a PDF file.
    Args:
        file_path (str): The path to the PDF file.
        max_pages (int, optional): The maximum number of pages to extract. Defaults to None (all pages).
    Returns:
        str: The extracted text.
    """
    with fitz.open(file_path) as doc:
        text = ''
        num_pages = len(doc)
        for page_num in range(num_pages):
            if max_pages is not None and page_num >= max_pages:
                break
            page = doc[page_num]
            text += page.get_text()
        return text


def extract_from_docx(file_path):
    """
    Extracts text from a DOCX file.
    Args:
        file_path (str): The path to the DOCX file.
    Returns:
        str: The extracted text.
    """
    doc = Document(file_path)
    text = ''
    for para in doc.paragraphs:
        text += para.text + '\n'
    return text


def extract_from_txt(file_path):
    """
    Extracts text from a raw text file.
    Args:
        file_path (str): The path to the raw text file.
    Returns:
        str: The extracted text.
    """
    text = ""
    
    with open(file_path) as f:
        text += f.read()

    return text


def extract_text(file_path, max_pages=None):
    """
    Extracts text from a file based on its extension.
    Args:
        file_path (str): The path to the file.
        max_pages (int, optional): The maximum number of pages to extract from PDFs. Defaults to None.
    Returns:
        str: The extracted text.
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == '.pdf':
        return extract_from_pdf(file_path, max_pages)
    elif file_extension == '.docx':
        return extract_from_docx(file_path)
    elif file_extension == '.txt':
        return extract_from_txt(file_path)
    else:
        print(f"Unsupported file format: {file_extension}")
        return None

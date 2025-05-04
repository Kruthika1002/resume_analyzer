import os
import PyPDF2
import docx
import re

def parse_resume(file_path):
    """
    Extract text from resume file (PDF or DOCX)
    
    Args:
        file_path (str): Path to the resume file
        
    Returns:
        str: Extracted text from the resume
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return parse_pdf(file_path)
    elif file_extension in ['.docx', '.doc']:
        return parse_docx(file_path)
    else:
        return "Unsupported file format. Please upload a PDF or DOCX file."

def parse_pdf(file_path):
    """Parse text from PDF file"""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
    except Exception as e:
        text = f"Error parsing PDF: {str(e)}"
    
    return clean_text(text)

def parse_docx(file_path):
    """Parse text from DOCX file"""
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        text = f"Error parsing DOCX: {str(e)}"
    
    return clean_text(text)

def clean_text(text):
    """Clean extracted text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters that might interfere with analysis
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()
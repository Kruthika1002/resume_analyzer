import os
import pytest
from utils.document_parser import parse_resume, parse_pdf, parse_docx, clean_text

# Define test files directory
TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")

# Create a test directory for sample files if it doesn't exist
os.makedirs(TEST_FILES_DIR, exist_ok=True)

# Sample PDF and DOCX content for testing
SAMPLE_PDF_TEXT = "This is a sample PDF resume."
SAMPLE_DOCX_TEXT = "This is a sample DOCX resume."

# Generate a sample PDF file
def create_sample_pdf(file_path, content):
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet

    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    content = Paragraph(content, styles['Normal'])
    doc.build([content])

# Generate a sample DOCX file
def create_sample_docx(file_path, content):
    from docx import Document

    doc = Document()
    doc.add_paragraph(content)
    doc.save(file_path)

@pytest.fixture(scope="module", autouse=True)
def setup_test_files():
    """Create test files for PDF and DOCX before running tests"""
    pdf_path = os.path.join(TEST_FILES_DIR, "sample_resume.pdf")
    docx_path = os.path.join(TEST_FILES_DIR, "sample_resume.docx")

    create_sample_pdf(pdf_path, SAMPLE_PDF_TEXT)
    create_sample_docx(docx_path, SAMPLE_DOCX_TEXT)

    yield

    # Cleanup after tests
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    if os.path.exists(docx_path):
        os.remove(docx_path)

def test_parse_resume_pdf():
    """Test parsing of a valid PDF file"""
    pdf_path = os.path.join(TEST_FILES_DIR, "sample_resume.pdf")
    result = parse_resume(pdf_path)
    assert SAMPLE_PDF_TEXT in result


def test_parse_resume_docx():
    """Test parsing of a valid DOCX file"""
    docx_path = os.path.join(TEST_FILES_DIR, "sample_resume.docx")
    result = parse_resume(docx_path)
    assert SAMPLE_DOCX_TEXT in result


def test_parse_resume_invalid_format():
    """Test parsing with unsupported file format"""
    result = parse_resume("invalid_file.txt")
    assert "Unsupported file format" in result


def test_clean_text_no_change():
    """Test clean_text with already clean text"""
    raw_text = "This is a clean text."
    result = clean_text(raw_text)
    assert result == raw_text



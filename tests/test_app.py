import os
import pytest
from app import app, allowed_file
from flask import session


@pytest.fixture
def client():
    """Set up Flask test client"""
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = 'test_uploads'
    app.secret_key = 'test_secret_key'  # Static secret for test
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    with app.test_client() as client:
        yield client

    # Clean up after tests
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
        os.rmdir(app.config['UPLOAD_FOLDER'])

def test_index_page(client):
    """Test if the index page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Upload your resume" in response.data
def test_allowed_file():
    """Test allowed file extensions"""
    assert allowed_file('resume.pdf') is True
    assert allowed_file('resume.docx') is True
    assert allowed_file('resume.doc') is True
    assert allowed_file('resume.txt') is False
    assert allowed_file('resume') is False
def test_upload_no_file(client):
    """Test file upload with no file provided and expect client-side validation"""
    response = client.get('/')
    assert response.status_code == 200  # Ensure the homepage loads correctly
    assert b"Please upload a resume file" in response.data

def test_upload_invalid_file_type(client):
    """Test upload with invalid file type and ensure it redirects correctly"""
    # Simulate invalid file type (.txt)
    data = {
        'resume': (b"Invalid content", 'invalid.txt'),  # Invalid file
        'job_description': 'Software Engineer'
    }

    # Send POST request to /upload
    response = client.post('/upload', data=data, content_type='multipart/form-data')

    # Check if the request is redirected to /upload
    assert response.status_code == 302  # Expecting a redirect
    assert '/upload' in response.headers['Location']  # Redirect to /upload

def test_results_page_no_data(client):
    """Test results page without session data"""
    response = client.get('/results')
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/')

def test_invalid_route(client):
    """Test accessing a non-existing route"""
    response = client.get('/non-existent-page')
    assert response.status_code == 404



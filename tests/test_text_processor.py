import pytest
from utils.text_processor import (
    extract_keywords,
    get_skills,
    identify_sections
    
)

@pytest.fixture
def sample_resume_text():
    """Provide sample resume text for testing"""
    return """
    John Doe
    john.doe@example.com | (123) 456-7890 | linkedin.com/in/johndoe
    
    Summary:
    Experienced software developer with expertise in Python, Flask, and REST APIs.
    
    Experience:
    Managed a team of 5 developers to create REST APIs using Flask.
    Increased application performance by 20% by optimizing SQL queries.
    
    Skills:
    Python, Flask, SQL, REST APIs, Docker, AWS, Git, NLP
    
    Education:
    Bachelor of Science in Computer Science
    XYZ University, 2022
    
    Projects:
    Developed a sentiment analysis system using NLP and Flask.
    """

@pytest.fixture
def incomplete_resume_text():
    """Provide incomplete resume text for testing"""
    return """
    Jane Smith
    janesmith@example.com
    
    Summary:
    Entry-level software engineer with basic knowledge of web development.
    
    Skills:
    Python, HTML, CSS, Web Development
    """

def test_extract_keywords(sample_resume_text):
    """Test keyword extraction using RAKE"""
    keywords = extract_keywords(sample_resume_text, top_n=5)
    assert len(keywords) > 0
    assert any("software developer" in kw for kw in keywords)
    assert any("rest apis" in kw for kw in keywords)

def test_get_skills(sample_resume_text):
    """Test skill extraction from resume text"""
    skills = get_skills(sample_resume_text)
    expected_skills = {'python', 'flask', 'sql', 'docker', 'aws', 'git', 'nlp'}
    assert set(skills) == expected_skills

def test_get_skills_incomplete_resume(incomplete_resume_text):
    """Test skill extraction from an incomplete resume"""
    skills = get_skills(incomplete_resume_text)
    expected_skills = {'python', 'html', 'css', 'web development'}
    assert set(skills) == expected_skills

def test_identify_sections(sample_resume_text):
    """Test section identification from a resume"""
    sections = identify_sections(sample_resume_text)
    
    assert 'summary' in sections
    assert 'experience' in sections
    assert 'skills' in sections
    assert 'education' in sections
    assert 'projects' in sections
    
    assert 'contact' not in sections  # Contact is not properly identified

def test_identify_sections_incomplete_resume(incomplete_resume_text):
    """Test section identification from an incomplete resume"""
    sections = identify_sections(incomplete_resume_text)
    
    assert 'summary' in sections
    assert 'skills' in sections
    assert 'experience' not in sections
    assert 'education' not in sections


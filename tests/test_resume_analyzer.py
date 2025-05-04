import pytest
from utils.resume_analyzer import (
    analyze_resume_sections,
    analyze_section_quality,
    analyze_resume_completeness,
    check_formatting_issues,
)

@pytest.fixture
def sample_resume():
    """Provide sample resume text for testing"""
    return """
    John Doe
    john.doe@example.com | (123) 456-7890 | linkedin.com/in/johndoe
    
    Summary:
    Experienced software developer with expertise in Python, Flask, and REST APIs.
    
    Experience:
    Developed REST APIs using Flask for multiple projects.
    Led a team of 5 developers to improve application performance by 20%.
    Created automated testing pipelines, reducing bugs by 15%.
    
    Skills:
    Python, Flask, SQL, REST APIs, Docker, AWS, Git
    
    Education:
    Bachelor of Science in Computer Science
    XYZ University, 2022
    
    Projects:
    Developed a real-time sentiment analysis system using NLP.
    """

@pytest.fixture
def incomplete_resume():
    """Provide an incomplete resume for testing"""
    return """
    John Doe
    john.doe@example.com
    
    Summary:
    Entry-level developer with a passion for coding.
    
    Skills:
    Python, HTML, CSS
    """

def test_analyze_resume_sections_incomplete_resume(incomplete_resume, mocker):
    """Test section analysis with an incomplete resume"""
    mocker.patch('utils.text_processor.identify_sections', return_value={
        'contact': 'john.doe@example.com',
        'summary': 'Entry-level developer with a passion for coding.',
        'skills': 'Python, HTML, CSS'
    })
    
    result = analyze_resume_sections(incomplete_resume)
    
    # Check missing essential and additional sections
    assert len(result['missing_essential']) > 0
    assert len(result['missing_additional']) > 0
    assert 'experience' in [item['section'] for item in result['missing_essential']]
    assert 'education' in [item['section'] for item in result['missing_essential']]

def test_analyze_resume_completeness_incomplete_resume(incomplete_resume):
    """Test completeness analysis for a short resume"""
    result = analyze_resume_completeness(incomplete_resume)
    
    assert result['word_count'] < 300
    assert any("Your resume is quite short" in rec for rec in result['general_recommendations'])

def test_check_formatting_issues_long_paragraph():
    """Test detection of long paragraphs"""
    long_paragraph_text = "This is a long paragraph with too many words that should be broken down " * 20
    recommendations = check_formatting_issues(long_paragraph_text)
    
    assert any("Break up long paragraphs" in rec for rec in recommendations)

def test_check_formatting_issues_uppercase():
    """Test detection of excessive uppercase words"""
    uppercase_text = "PYTHON FLASK API AWS EXCELLENT SKILLS ARE REQUIRED FOR THIS ROLE."
    recommendations = check_formatting_issues(uppercase_text)
    
    assert any("Avoid excessive use of ALL CAPS" in rec for rec in recommendations)

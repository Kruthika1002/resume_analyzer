import pytest
from utils.job_matcher import match_resume_to_job, generate_recommendations

@pytest.fixture
def sample_data():
    """Provide sample resume and job description for testing"""
    resume_text = """
    Experienced Python Developer with strong knowledge of Flask, Django, and REST APIs.
    Proficient in SQL, data analysis, and cloud deployment using AWS. Skilled in unit testing and version control.
    """
    job_description = """
    We are looking for a Python Developer with experience in Flask and Django. 
    Knowledge of REST APIs, SQL, and cloud platforms like AWS is preferred. 
    Strong understanding of unit testing and version control systems is required.
    """
    return resume_text, job_description

def test_match_resume_to_job_no_keywords(mocker):
    """Test with no matching keywords"""
    resume_text = "Basic knowledge of Microsoft Word and Excel."
    job_description = "Looking for Python Developer with Flask, SQL, and AWS experience."

    # Mock extract_keywords and get_skills
    mocker.patch('utils.text_processor.extract_keywords', side_effect=lambda text: text.lower().split())
    mocker.patch('utils.text_processor.get_skills', side_effect=lambda text: set())

    result = match_resume_to_job(resume_text, job_description)

    # Check no matching skills or keywords
    assert result['keyword_match_percentage'] == 0
    assert result['skill_match_percentage'] == 0
    assert len(result['missing_skills']) > 0
    assert len(result['recommendations']) > 0


def test_generate_recommendations_high_match():
    """Test recommendations for high match scores"""
    recommendations = generate_recommendations(
        keyword_match=80,
        skill_match=90,
        missing_skills=set(),
        missing_terms=[]
    )
    assert any("well-aligned" in rec for rec in recommendations)


def test_generate_recommendations_low_match():
    """Test recommendations for low match scores"""
    recommendations = generate_recommendations(
        keyword_match=20,
        skill_match=25,
        missing_skills={"Django", "SQL"},
        missing_terms=[{"term": "testing", "frequency": 5}, {"term": "API", "frequency": 3}]
    )
    assert any("low keyword alignment" in rec for rec in recommendations)
    assert any("Consider adding these missing skills" in rec for rec in recommendations)
    assert any("important terms appear frequently" in rec for rec in recommendations)

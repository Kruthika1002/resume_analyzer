import re
import nltk
from rake_nltk import Rake
import spacy
from collections import Counter

# Download necessary NLTK data
try:
    nltk.data.find('punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('stopwords')
except LookupError:
    nltk.download('stopwords')

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import sys
    import subprocess
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def extract_keywords(text, top_n=20):
    """
    Extract important keywords from text using RAKE algorithm
    
    Args:
        text (str): Input text
        top_n (int): Number of top keywords to return
        
    Returns:
        list: List of top keywords
    """
    rake = Rake()
    rake.extract_keywords_from_text(text)
    keywords = rake.get_ranked_phrases()[:top_n]
    return keywords

def get_skills(text):
    """
    Extract potential skills from text using predefined skill words and phrases
    
    Args:
        text (str): Input text
        
    Returns:
        list: List of identified skills
    """
    # Common tech skills and keywords
    common_skills = [
        # Programming languages
        "python", "java", "javascript", "c\\+\\+", "c#", "ruby", "php", "swift", "kotlin", "go", "rust",
        "typescript", "scala", "perl", "r", "matlab", "bash", "shell", "sql", "nosql",
        
        # Web technologies
        "html", "css", "react", "angular", "vue", "node", "express", "django", "flask", "spring", 
        "asp\\.net", "laravel", "ruby on rails", "jquery", "bootstrap", "tailwind",
        
        # Data science & ML
        "machine learning", "deep learning", "data science", "neural networks", "nlp", 
        "natural language processing", "computer vision", "tensorflow", "pytorch", "keras", 
        "scikit-learn", "pandas", "numpy", "data mining", "statistics", "big data",
        
        # Cloud & DevOps
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "ci/cd", "jenkins", 
        "terraform", "ansible", "devops", "cloud computing", "microservices",
        
        # Databases
        "mysql", "postgresql", "mongodb", "sqlite", "oracle", "sql server", "redis", "elasticsearch",
        "dynamodb", "cassandra", "firebase",
        
        # Mobile
        "android", "ios", "react native", "flutter", "xamarin", "mobile development",
        
        # General tech
        "git", "github", "bitbucket", "jira", "agile", "scrum", "rest api", "graphql", "oauth", 
        "jwt", "authentication", "authorization", "responsive design", "web development",
        "software engineering", "quality assurance", "testing", "unit testing", "integration testing",
        
        # Soft skills
        "leadership", "teamwork", "communication", "problem solving", "critical thinking",
        "time management", "project management", "presentation", "collaboration"
    ]
    
    # Create a regex pattern that matches whole words
    pattern = r'\b(' + '|'.join(common_skills) + r')\b'
    found_skills = re.findall(pattern, text.lower())
    
    # Count occurrences and return the unique skills
    return list(set(found_skills))

def identify_sections(text):
    """
    Identify common resume sections
    
    Args:
        text (str): Resume text
        
    Returns:
        dict: Dictionary of identified sections
    """
    # Common resume section headers
    sections = {
        'education': ['education', 'academic background', 'academic history', 'qualifications', 'degrees'],
        'experience': ['experience', 'work experience', 'employment history', 'work history', 'professional experience'],
        'skills': ['skills', 'technical skills', 'core competencies', 'competencies', 'expertise'],
        'projects': ['projects', 'project experience', 'key projects', 'academic projects'],
        'certifications': ['certifications', 'certificates', 'professional certifications'],
        'summary': ['summary', 'professional summary', 'career summary', 'profile', 'objective'],
        'contact': ['contact', 'contact information', 'personal details', 'personal information'],
        'languages': ['languages', 'language proficiency', 'language skills'],
        'awards': ['awards', 'honors', 'achievements', 'recognitions'],
        'publications': ['publications', 'research', 'papers', 'articles']
    }
    
    found_sections = {}
    lines = text.lower().split('\n')
    
    for i, line in enumerate(lines):
        for section_name, keywords in sections.items():
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', line):
                    start_index = i
                    # Try to find the next section header to determine end of current section
                    end_index = len(lines)
                    for j in range(i+1, len(lines)):
                        for other_section, other_keywords in sections.items():
                            if section_name != other_section:
                                for other_keyword in other_keywords:
                                    if re.search(r'\b' + re.escape(other_keyword) + r'\b', lines[j]):
                                        end_index = j
                                        break
                                if end_index < len(lines):
                                    break
                        if end_index < len(lines):
                            break
                    
                    # Extract section content
                    section_content = '\n'.join(lines[start_index:end_index])
                    found_sections[section_name] = section_content
                    break
    
    return found_sections

def extract_entities(text):
    """
    Extract named entities (organizations, dates, etc.) using spaCy
    
    Args:
        text (str): Input text
        
    Returns:
        dict: Dictionary of extracted entities by type
    """
    doc = nlp(text)
    entities = {
        'organizations': [],
        'dates': [],
        'locations': [],
        'titles': []
    }
    
    for ent in doc.ents:
        if ent.label_ == 'ORG':
            entities['organizations'].append(ent.text)
        elif ent.label_ == 'DATE':
            entities['dates'].append(ent.text)
        elif ent.label_ == 'GPE' or ent.label_ == 'LOC':
            entities['locations'].append(ent.text)
        elif ent.label_ == 'PERSON':
            entities['titles'].append(ent.text)
    
    # Remove duplicates
    for key in entities:
        entities[key] = list(set(entities[key]))
    
    return entities
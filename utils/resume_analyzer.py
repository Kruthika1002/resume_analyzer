import re
from utils.text_processor import identify_sections, get_skills, extract_entities

def analyze_resume_sections(resume_text):
    """
    Analyze the resume for missing or weak sections
    
    Args:
        resume_text (str): Text extracted from the resume
        
    Returns:
        dict: Analysis results with recommendations
    """
    # Identify sections in the resume
    sections = identify_sections(resume_text)
    
    # Define essential sections for a resume
    essential_sections = {
        'contact': 'Contact information is crucial for employers to reach you',
        'summary': 'A professional summary gives a quick overview of your qualifications',
        'education': 'Education details establish your academic background',
        'experience': 'Work experience demonstrates your practical skills and achievements',
        'skills': 'A skills section highlights your core competencies'
    }
    
    # Additional useful sections
    additional_sections = {
        'projects': 'Projects showcase your practical application of skills',
        'certifications': 'Certifications validate your expertise in specific areas',
        'awards': 'Awards highlight your achievements and recognition',
        'languages': 'Language skills can be valuable for certain positions',
        'publications': 'Publications demonstrate expertise and thought leadership'
    }
    
    analysis = {
        'missing_essential': [],
        'missing_additional': [],
        'present_sections': [],
        'section_quality': {}
    }
    
    # Check for missing essential sections
    for section, description in essential_sections.items():
        if section not in sections:
            analysis['missing_essential'].append({
                'section': section,
                'description': description
            })
        else:
            analysis['present_sections'].append(section)
            # Analyze section quality
            quality = analyze_section_quality(section, sections[section])
            analysis['section_quality'][section] = quality
    
    # Check for missing additional sections
    for section, description in additional_sections.items():
        if section not in sections:
            analysis['missing_additional'].append({
                'section': section,
                'description': description
            })
        elif section not in analysis['present_sections']:
            analysis['present_sections'].append(section)
            # Analyze section quality
            quality = analyze_section_quality(section, sections[section])
            analysis['section_quality'][section] = quality
    
    return analysis

def analyze_section_quality(section_name, section_content):
    """
    Analyze the quality of a specific resume section
    
    Args:
        section_name (str): Name of the section
        section_content (str): Content of the section
        
    Returns:
        dict: Quality analysis with recommendations
    """
    words = section_content.strip().split()
    word_count = len(words)
    
    quality = {
        'length': word_count,
        'recommendations': []
    }
    
    # Length-based recommendations
    if section_name == 'summary':
        if word_count < 30:
            quality['recommendations'].append("Your summary is brief. Consider expanding it to 50-100 words to better highlight your key qualifications.")
        elif word_count > 200:
            quality['recommendations'].append("Your summary is quite long. Consider condensing it to 50-100 words for better readability.")
    
    elif section_name == 'experience':
        if word_count < 100:
            quality['recommendations'].append("Your experience section appears thin. Add more details about your responsibilities and achievements.")
        
        # Check for action verbs
        action_verbs = ["managed", "developed", "created", "implemented", "led", "designed", "coordinated", 
                         "achieved", "improved", "increased", "reduced", "analyzed", "organized", "delivered"]
        has_action_verbs = any(verb in section_content.lower() for verb in action_verbs)
        
        if not has_action_verbs:
            quality['recommendations'].append("Use strong action verbs to describe your achievements (e.g., 'managed', 'developed', 'improved').")
        
        # Check for metrics and achievements
        has_metrics = any(char in section_content for char in "%$")
        has_numbers = any(char.isdigit() for char in section_content)
        
        if not has_metrics and not has_numbers:
            quality['recommendations'].append("Add quantifiable achievements and metrics to demonstrate your impact (e.g., 'increased sales by 20%').")
    
    elif section_name == 'skills':
        # Extract skills
        skills = get_skills(section_content)
        skill_count = len(skills)
        
        if skill_count < 5:
            quality['recommendations'].append(f"You've listed only {skill_count} recognizable skills. Add more relevant technical and soft skills.")
        
        quality['identified_skills'] = skills
    
    elif section_name == 'education':
        entities = extract_entities(section_content)
        
        if not entities['organizations']:
            quality['recommendations'].append("Ensure your education section clearly mentions institution names.")
            
        if not entities['dates']:
            quality['recommendations'].append("Include graduation dates or attendance periods in your education section.")
    
    # General recommendations
    if word_count < 10 and section_name not in ['contact', 'languages']:
        quality['recommendations'].append(f"Your {section_name} section is very brief. Consider adding more details.")
    
    return quality

def analyze_resume_completeness(resume_text):
    """
    Analyze overall resume completeness and quality
    
    Args:
        resume_text (str): Text extracted from the resume
        
    Returns:
        dict: Overall analysis with recommendations
    """
    word_count = len(resume_text.split())
    
    analysis = {
        'word_count': word_count,
        'general_recommendations': []
    }
    
    # Word count recommendations
    if word_count < 300:
        analysis['general_recommendations'].append("Your resume is quite short. A typical resume is 400-800 words.")
    elif word_count > 1000:
        analysis['general_recommendations'].append("Your resume is lengthy. Consider condensing it to 1-2 pages (400-800 words).")
    
    # Check for email and phone
    has_email = bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', resume_text))
    has_phone = bool(re.search(r'(\+\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}', resume_text))
    
    if not has_email:
        analysis['general_recommendations'].append("Add your email address to your contact information.")
    if not has_phone:
        analysis['general_recommendations'].append("Add your phone number to your contact information.")
    
    # Check for LinkedIn profile
    has_linkedin = 'linkedin.com' in resume_text.lower()
    if not has_linkedin:
        analysis['general_recommendations'].append("Consider adding your LinkedIn profile to your contact information.")
    
    # Check for formatting issues
    formatting_issues = check_formatting_issues(resume_text)
    analysis['general_recommendations'].extend(formatting_issues)
    
    return analysis

def check_formatting_issues(text):
    """
    Check for common formatting issues in the resume
    
    Args:
        text (str): Resume text
        
    Returns:
        list: Formatting recommendations
    """
    recommendations = []
    
    # Check for very long paragraphs
    paragraphs = text.split('\n\n')
    for paragraph in paragraphs:
        if len(paragraph.split()) > 100:
            recommendations.append("Break up long paragraphs into smaller, more readable sections.")
            break
    
    # Check for overuse of capitalization
    uppercase_words = sum(1 for word in text.split() if word.isupper() and len(word) > 1)
    if uppercase_words > 20 or (uppercase_words / len(text.split()) > 0.1):
        recommendations.append("Avoid excessive use of ALL CAPS as it can make your resume harder to read.")
    
    return recommendations
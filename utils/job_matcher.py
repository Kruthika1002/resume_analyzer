from utils.text_processor import extract_keywords, get_skills
import re
from collections import Counter

def match_resume_to_job(resume_text, job_description):
    """
    Match resume against job description and provide recommendations
    
    Args:
        resume_text (str): Text extracted from the resume
        job_description (str): Job description text
        
    Returns:
        dict: Matching results and recommendations
    """
    # Extract keywords from both texts
    resume_keywords = set(extract_keywords(resume_text))
    job_keywords = set(extract_keywords(job_description))
    
    # Calculate keyword match percentage
    matching_keywords = resume_keywords.intersection(job_keywords)
    keyword_match_percentage = len(matching_keywords) / len(job_keywords) * 100 if job_keywords else 0
    
    # Extract skills from both
    resume_skills = set(get_skills(resume_text))
    job_skills = set(get_skills(job_description))
    
    # Calculate skill match percentage
    matching_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills - resume_skills
    skill_match_percentage = len(matching_skills) / len(job_skills) * 100 if job_skills else 0
    
    # Overall match score (weighted average)
    overall_match = (keyword_match_percentage * 0.4) + (skill_match_percentage * 0.6)
    
    # Identify frequently mentioned terms in job description that are absent in resume
    job_words = re.findall(r'\b\w+\b', job_description.lower())
    word_counts = Counter(job_words)
    
    # Filter out common stop words
    common_words = {"a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "with", 
                   "by", "about", "as", "of", "that", "this", "these", "those", "is", "are", 
                   "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", 
                   "did", "will", "shall", "should", "can", "could", "may", "might", "must", 
                   "we", "you", "they", "he", "she", "it", "i", "me", "him", "her", "them", "us"}
    
    # Get important job terms (mentioned 3+ times) that are missing from resume
    missing_terms = []
    for word, count in word_counts.items():
        if count >= 3 and len(word) > 3 and word not in common_words:
            if word not in resume_text.lower():
                missing_terms.append({"term": word, "frequency": count})
    
    # Sort by frequency
    missing_terms.sort(key=lambda x: x["frequency"], reverse=True)
    
    # Generate recommendations based on the analysis
    recommendations = generate_recommendations(
        keyword_match_percentage, 
        skill_match_percentage, 
        missing_skills, 
        missing_terms[:10]  # Top 10 missing terms
    )
    
    return {
        'keyword_match_percentage': round(keyword_match_percentage, 1),
        'skill_match_percentage': round(skill_match_percentage, 1),
        'overall_match': round(overall_match, 1),
        'matching_keywords': list(matching_keywords),
        'matching_skills': list(matching_skills),
        'missing_skills': list(missing_skills),
        'missing_terms': missing_terms[:10],  # Top 10 missing terms
        'recommendations': recommendations
    }

def generate_recommendations(keyword_match, skill_match, missing_skills, missing_terms):
    """
    Generate tailored recommendations based on the analysis
    
    Args:
        keyword_match (float): Keyword match percentage
        skill_match (float): Skill match percentage
        missing_skills (set): Set of missing skills
        missing_terms (list): List of missing important terms
        
    Returns:
        list: Tailored recommendations
    """
    recommendations = []
    
    # Keyword match recommendations
    if keyword_match < 30:
        recommendations.append("Your resume has low keyword alignment with the job description. Try incorporating more relevant terminology from the job posting.")
    elif keyword_match < 60:
        recommendations.append("Your resume has moderate keyword alignment. Incorporate more specific terminology from the job description to improve matching.")
    
    # Skill match recommendations
    if skill_match < 40:
        if missing_skills:
            skill_rec = "Consider adding these missing skills to your resume (if you possess them): " + ", ".join(list(missing_skills)[:5])
            if len(missing_skills) > 5:
                skill_rec += f", and {len(missing_skills) - 5} more"
            recommendations.append(skill_rec)
    
    # Missing terms recommendations
    if missing_terms:
        terms_rec = "These important terms appear frequently in the job description but are missing from your resume: "
        terms_list = [f"{term['term']} ({term['frequency']} mentions)" for term in missing_terms[:5]]
        terms_rec += ", ".join(terms_list)
        if len(missing_terms) > 5:
            terms_rec += f", and {len(missing_terms) - 5} more"
        recommendations.append(terms_rec)
    
    # General advice based on match scores
    overall_score = (keyword_match + skill_match) / 2
    if overall_score < 30:
        recommendations.append("Your resume needs significant customization for this job. Consider restructuring and highlighting relevant experience and skills.")
    elif overall_score < 50:
        recommendations.append("Your resume partially matches this job. Highlight your most relevant experiences more prominently.")
    elif overall_score < 70:
        recommendations.append("Your resume is fairly well-aligned with this job. Make targeted adjustments to emphasize your most relevant qualifications.")
    else:
        recommendations.append("Your resume is well-aligned with this job! Consider fine-tuning to emphasize your strongest qualifications even more.")
    
    return recommendations
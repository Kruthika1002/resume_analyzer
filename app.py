import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.utils import secure_filename
import uuid

from utils.document_parser import parse_resume
from utils.resume_analyzer import analyze_resume_sections, analyze_resume_completeness
from utils.job_matcher import match_resume_to_job
from utils.text_processor import extract_keywords

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'doc'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return redirect(request.url)
    
    resume_file = request.files['resume']
    job_description = request.form.get('job_description', '')
    
    if resume_file.filename == '':
        return redirect(request.url)
    
    if resume_file and allowed_file(resume_file.filename):
        # Generate a unique filename
        filename = secure_filename(resume_file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save the file
        resume_file.save(filepath)
        
        # Process the resume
        resume_text = parse_resume(filepath)
        
        # Analyze the resume
        sections_analysis = analyze_resume_sections(resume_text)
        completeness_analysis = analyze_resume_completeness(resume_text)
        
        # Match against job description
        job_match_results = {}
        if job_description:
            job_match_results = match_resume_to_job(resume_text, job_description)
        
        # Store results in session
        session['analysis_results'] = {
            'sections': sections_analysis,
            'completeness': completeness_analysis,
            'job_match': job_match_results,
            'resume_text': resume_text[:1000] + '...' if len(resume_text) > 1000 else resume_text
        }
        
        # Clean up the file
        os.remove(filepath)
        
        return redirect(url_for('results'))
    
    return redirect(request.url)

@app.route('/results')
def results():
    analysis_results = session.get('analysis_results', {})
    if not analysis_results:
        return redirect(url_for('index'))
    
    return render_template('results.html', results=analysis_results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 

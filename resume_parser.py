import json
import re
import fitz  # PyMuPDF
import docx
import pandas as pd

def parse_resume(text):
    # Define regex patterns to extract information
    patterns = {
        'name': r'Name:\s*(.*)',
        'email': r'Email:\s*(.*)',
        'phone': r'Phone:\s*(.*)',
        'address': r'Address:\s*(.*)',
        'education': r'Education:\n((?:- .*\n)*)',
        'experience': r'Experience:\n((?:- .*\n)*)',
        'skills': r'Skills:\n((?:- .*\n)*)'
    }
    
    resume_data = {}
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            if key in ['education', 'experience', 'skills']:
                # Split multi-line entries into a list
                resume_data[key] = [line.strip('- ') for line in match.group(1).strip().split('\n')]
            else:
                resume_data[key] = match.group(1).strip()
    
    return resume_data

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_csv(file_path):
    df = pd.read_csv(file_path)
    text = df.to_string(index=False)
    return text

def read_resume(file_path, file_type):
    if file_type == 'pdf':
        text = extract_text_from_pdf(file_path)
    elif file_type == 'docx':
        text = extract_text_from_docx(file_path)
    elif file_type == 'csv':
        text = extract_text_from_csv(file_path)
    else:
        raise ValueError("Unsupported file type. Please use 'pdf', 'docx', or 'csv'.")
    
    return text

def main(file_path, file_type):
    # Read resume based on the file type
    resume_text = read_resume(file_path, file_type)
    
    # Parse the resume
    parsed_resume = parse_resume(resume_text)
    
    # Convert to JSON
    resume_json = json.dumps(parsed_resume, indent=4)
    
    # Output JSON
    print(resume_json)

# Example usage:
# main('path/to/resume.pdf', 'pdf')
# main('path/to/resume.docx', 'docx')
# main('path/to/resume.csv', 'csv')

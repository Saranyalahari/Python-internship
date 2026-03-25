from preprocess import clean_text
from extractors import extract_email, extract_skills, extract_education, extract_experience


def parse_resume(text):

    text = clean_text(text)

    data = {

        "email": extract_email(text),

        "skills": extract_skills(text),

        "education": extract_education(text),

        "experience": extract_experience(text)
    }

    return data
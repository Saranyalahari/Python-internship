import re

def clean_text(text):

    text = re.sub(r'\s+', ' ', text)  # remove extra spaces
    text = text.replace('\n', ' ')
    text = text.strip()

    return text
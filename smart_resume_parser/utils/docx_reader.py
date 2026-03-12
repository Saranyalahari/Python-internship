from docx import Document

def extract_text_from_docx(file):

    doc = Document(file)

    text = []

    for para in doc.paragraphs:
        text.append(para.text)

    return "\n".join(text)
import fitz

def extract_text_from_pdf(pdf_path):
    text = ""

    try:
        doc = fitz.open(pdf_path)

        for page in doc:
            page_text = page.get_text()

            if page_text.strip():  # handle empty pages
                text += page_text + "\n"

        doc.close()

    except Exception as e:
        print("Error reading PDF:", e)

    return text
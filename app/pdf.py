import pdfplumber


def extract_text_from_pdf(path):
    text_all = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text_all += t + "\n"
    return text_all

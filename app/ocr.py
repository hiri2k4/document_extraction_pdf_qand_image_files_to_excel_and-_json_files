import pytesseract
import cv2

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def preprocess_image(path):
    img = cv2.imread(path)

    if img is None:
        raise ValueError(f"Unable to read image: {path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    return gray


def extract_text_from_image(path):
    img = preprocess_image(path)
    text = pytesseract.image_to_string(img, config="--psm 6")
    return text

from ocr import extract_text_from_image
from pdf import extract_text_from_pdf
from table import extract_items_table_from_pdf
from field import classify_document, extract_invoice_fields, extract_packing_fields


def process_document(path):

    if path.lower().endswith(".pdf"):
        text = extract_text_from_pdf(path)
        items_df = extract_items_table_from_pdf(path)
    else:
        text = extract_text_from_image(path)
        items_df = None

    doc_type = classify_document(text)

    if doc_type == "Invoice":
        fields = extract_invoice_fields(text)
    elif doc_type == "Packing List":
        fields = extract_packing_fields(text)
    else:
        fields = {}

    return doc_type, fields, items_df

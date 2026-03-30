import re


def classify_document(text):
    t = text.lower()

    if "packing list" in t or "ship qty" in t:
        return "Packing List"

    if "invoice" in t:
        return "Invoice"

    return "Unknown"


def extract_date(text):
    patterns = [
        r"\d{2}[/-]\d{2}[/-]\d{4}",
        r"\d{4}[/-]\d{2}[/-]\d{2}",
        r"\d{2}\s[A-Za-z]+\s\d{4}",
        r"[A-Za-z]+\s\d{1,2},?\s\d{4}"
    ]

    for pat in patterns:
        m = re.search(pat, text)
        if m:
            return m.group(0)

    return ""


def extract_invoice_number(text):

    patterns = [
        r"Invoice\s*(No|Number|#|No.)\s*[:\-]?\s*([A-Za-z0-9\-\/]+)",
        r"Inv\s*(No|#)?\s*[:\-]?\s*([A-Za-z0-9\-\/]+)",
        r"Bill\s*No\s*[:\-]?\s*([A-Za-z0-9\-\/]+)"
    ]

    for pat in patterns:
        m = re.search(pat, text, re.I)
        if m:
            return m.group(m.lastindex)

    return ""


def extract_invoice_fields(text):

    fields = {
        "Vendor Name": "",
        "Invoice Number": "",
        "Invoice Date": ""
    }

    fields["Invoice Number"] = extract_invoice_number(text)
    fields["Invoice Date"] = extract_date(text)

    lines = [l.strip() for l in text.split("\n") if l.strip()]
    ignore = ["invoice","gst","phone","email","bill to","ship to","date"]

    for line in lines[:20]:
        lower = line.lower()

        if any(word in lower for word in ignore):
            continue

        if len(line) < 4:
            continue

        if sum(c.isdigit() for c in line) > len(line) * 0.3:
            continue

        fields["Vendor Name"] = line
        break

    return fields


def extract_packing_fields(text):

    fields = {
        "Order Number": "",
        "Ship To": ""
    }

    order_patterns = [
        r"Order\s*(No|Number|#)\s*[:\-]?\s*([A-Za-z0-9\-\/]+)",
        r"PO\s*(No|#)?\s*[:\-]?\s*([A-Za-z0-9\-\/]+)"
    ]

    for pat in order_patterns:
        m = re.search(pat, text, re.I)
        if m:
            fields["Order Number"] = m.group(m.lastindex)
            break

    lines = text.split("\n")
    capture = False
    ship_lines = []

    for line in lines:
        lower = line.lower()

        if "ship to" in lower:
            capture = True
            continue

        if capture:
            if any(word in lower for word in ["invoice","order","description","qty","total"]):
                break
            if line.strip():
                ship_lines.append(line.strip())
            if len(ship_lines) >= 5:
                break

    fields["Ship To"] = " ".join(ship_lines)
    return fields

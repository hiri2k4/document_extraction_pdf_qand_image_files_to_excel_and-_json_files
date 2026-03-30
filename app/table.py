import pandas as pd
from pdf import extract_text_from_pdf


def clean_dataframe(df):
    df = df.dropna(axis=1, how="all")
    df = df.fillna("")

    df.columns = [
        str(c).strip() if str(c).strip() else f"Column_{i+1}"
        for i, c in enumerate(df.columns)
    ]

    df = df[~df.apply(
        lambda row: row.astype(str)
        .str.lower()
        .str.contains("total|cgst|sgst|igst|tax|amount")
        .any(),
        axis=1
    )]

    return df


def fallback_extract_items_from_text(text):

    lines = text.split("\n")
    rows = []
    capture = False

    for line in lines:
        lower = line.lower()

        if any(word in lower for word in ["description","item","qty","quantity"]):
            capture = True
            continue

        if capture:
            if any(word in lower for word in ["total","cgst","sgst","igst","tax"]):
                break

            if len(line.strip()) > 5:
                rows.append([line.strip()])

    if rows:
        return pd.DataFrame(rows, columns=["Items"])

    return None


import pdfplumber

def extract_items_table_from_pdf(path):

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

            for table in tables:
                if not table or len(table) < 2:
                    continue

                header_text = " ".join(str(x).lower() for x in table[0] if x)

                if any(word in header_text for word in
                       ["item","description","qty","quantity","part"]):

                    df = pd.DataFrame(table[1:], columns=table[0])
                    df = clean_dataframe(df)

                    if len(df) > 0:
                        return df

    text = extract_text_from_pdf(path)
    return fallback_extract_items_from_text(text)

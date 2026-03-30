import streamlit as st
import pandas as pd
import tempfile
import json
import os
import time
from init import process_document

# PAGE CONFIG
st.set_page_config(
    page_title="Document Extraction to Excel & JSON Files",
    layout="wide"
)

# CUSTOM STYLE
st.markdown("""
<style>
.main-title {
    font-size:54px;
    font-weight:800;
    color:#4FC3F7;
}
.subtitle {
    font-size:20px;
    color:#bbbbbb;
    margin-bottom:20px;
}
.section-title {
    font-size:26px;
    font-weight:700;
    margin-top:25px;
}
.kpi-card {
    background-color:#1f2937;
    padding:18px;
    border-radius:12px;
    text-align:center;
}
.kpi-number {
    font-size:28px;
    font-weight:bold;
    color:#4FC3F7;
}
.kpi-label {
    font-size:16px;
    color:#cccccc;
}
.footer {
    text-align:center;
    font-size:15px;
    margin-top:40px;
    color:#888888;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="main-title">Document Extraction to Excel & JSON Files</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Developed by Hiri Karan M</div>', unsafe_allow_html=True)

st.info("Extract structured data from invoices and packing lists (PDF & Images).")

# KPI DASHBOARD
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="kpi-card"><div class="kpi-number">10</div><div class="kpi-label">Days Development</div></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="kpi-card"><div class="kpi-number">PDF + Image</div><div class="kpi-label">Formats Supported</div></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="kpi-card"><div class="kpi-number">OCR</div><div class="kpi-label">Tesseract Used</div></div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="kpi-card"><div class="kpi-number">Excel + JSON</div><div class="kpi-label">Output Formats</div></div>', unsafe_allow_html=True)

# DEVELOPMENT EFFORT
st.markdown('<div class="section-title">Development Effort Distribution</div>', unsafe_allow_html=True)

effort_data = {
    "Technology": [
        "OCR + Image Processing",
        "PDF Parsing (pdfplumber)",
        "Field Extraction Logic",
        "Table Extraction",
        "Dashboard UI",
        "Testing & Validation"
    ],
    "Days": [2, 2, 2, 2, 1, 1]
}

df_effort = pd.DataFrame(effort_data)
st.bar_chart(df_effort.set_index("Technology"))

# SIDEBAR
st.sidebar.header("Project Overview")

st.sidebar.markdown("""
### Tools & Technologies
- Python  
- Tesseract OCR  
- OpenCV  
- pdfplumber  
- Pandas  
- Streamlit  
""")

st.sidebar.markdown("### GitHub Repository")
st.sidebar.markdown("[View Project on GitHub](https://github.com/vh12342cse22-lgtm)")

# FILE UPLOAD
st.markdown('<div class="section-title">Upload Document</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Invoice or Packing List",
    type=["pdf", "png", "jpg", "jpeg"]
)

# DOCUMENT PREVIEW
if uploaded_file is not None:
    st.markdown('<div class="section-title">Document Preview</div>', unsafe_allow_html=True)

    file_type = uploaded_file.type

    if "image" in file_type:
        st.image(uploaded_file, use_container_width=True)

    elif "pdf" in file_type:
        st.write("PDF uploaded. Preview not fully supported in Streamlit, but extraction will process it.")

# PROCESS DOCUMENT
if uploaded_file is not None:

    file_extension = uploaded_file.name.split(".")[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    if st.button("Extract Data"):

        progress_bar = st.progress(0)

        for percent in range(0, 90, 10):
            time.sleep(0.05)
            progress_bar.progress(percent)

        doc_type, fields, items_df = process_document(temp_path)

        progress_bar.progress(100)

        st.success(f"Document Type Detected: {doc_type}")

        # SUMMARY
        st.markdown('<div class="section-title">Summary</div>', unsafe_allow_html=True)
        summary_df = pd.DataFrame([fields])
        st.dataframe(summary_df, use_container_width=True)

        # ITEMS
        st.markdown('<div class="section-title">Items Table</div>', unsafe_allow_html=True)

        if items_df is not None and len(items_df) > 0:
            st.dataframe(items_df, use_container_width=True)
        else:
            st.info("Items table not detected or not applicable.")

        # DOWNLOAD
        st.markdown('<div class="section-title">Download Results</div>', unsafe_allow_html=True)

        json_data = json.dumps(fields, indent=4)
        st.download_button("Download JSON", json_data, file_name="extracted_data.json")

        excel_path = "temp_output.xlsx"
        with pd.ExcelWriter(excel_path) as writer:
            summary_df.to_excel(writer, sheet_name="Summary", index=False)
            if items_df is not None and len(items_df) > 0:
                items_df.to_excel(writer, sheet_name="Items", index=False)

        with open(excel_path, "rb") as f:
            st.download_button("Download Excel", f, file_name="extracted_data.xlsx")

# FOOTER
st.markdown('<div class="footer">Developed by Hiri Karan M • Document Extraction Internship Project</div>', unsafe_allow_html=True)



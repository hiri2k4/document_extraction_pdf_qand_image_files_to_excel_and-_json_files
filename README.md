# Document Extraction Service
A local-first application to classify and extract data from invoices and packing lists.

## Overview
This project is a Document Extraction System that processes Invoices and Packing Lists from PDF and Image files and converts them into structured data.

## The system performs:
*Document classification
*Field extraction
*Table extraction
*Export to Excel and JSON
*All processing is done locally without external APIs.

## Features
*Invoice and Packing List detection
*Extraction of key fields
*Line item table extraction
*JSON and Excel output
*Streamlit-based UI

## Technology Stack
*Python
*Streamlit
*Tesseract OCR
*OpenCV
*pdfplumber
*Pandas

## Project Structure
app/        → Source code  
samples/    → Sample documents  
output/     → Extraction results  
design/     → Flowchart and architecture diagrams  
resume/     → Resume PDF  
README.md

## How to Run
*Install dependencies:
pip install streamlit pandas opencv-python pytesseract pdfplumber pillow
*Install Tesseract OCR and set the path if needed.
*Run the application:
streamlit run app.py

## Workflow
*Upload document
*Extract text (OCR or PDF parser)
*Classify document
*Extract fields and tables
*Generate JSON and Excel output

## Author
Hiri Karan M
B.E Computer Science and Engineering

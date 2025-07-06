# 🧾 Receipt Processing Automation App

A Flask-based web application to automate the upload and processing of scanned receipt PDFs. It uses Hugging Face’s LayoutLM model for OCR and extracts structured data like merchant name, total amount, and purchase date.

---

## 📌 Project Overview

This application:
- Accepts receipt PDFs via API.
- Validates if uploaded files are actual PDFs.
- Converts the first page of each PDF to an image.
- Uses a transformer-based document QA model to extract key data.
- Stores both file metadata and extracted info into a local SQLite database.
- Exposes REST APIs to interact with receipts.

---

## 🔍 Technologies Used

- **Python 3.10+**
- **Flask**
- **SQLAlchemy (SQLite)**
- **pdf2image + Poppler**
- **transformers (Hugging Face)**
- **LayoutLMv1 (`impira/layoutlm-document-qa`)**

---

## 📁 Folder Structure

receipt_automation/
├── app.py # Main Flask application entry
├── config.py # Flask + DB configuration
├── models.py # SQLAlchemy models
├── routes.py # All API endpoints
├── ocr_utils.py # OCR logic using Hugging Face model
├── requirements.txt # Python dependencies
├── .gitignore # Git ignore rules
├── README.md # This file
├── db/
│ └── receipts.db # SQLite database
└── receipts/
└── sample1.pdf # Sample PDF receipts


---

## ⚙️ Setup Instructions

### 1. Clone the Repo & Create a Virtual Environment

```bash
git clone <your-repo-url>
cd receipt_automation
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
brew install poppler

python app.py


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

### 1. Clone the Repo & Create a Virtual Environment & install popple & run the application

```bash
git clone https://github.com/mohammed-muzzammil/reciept-automation.git
cd receipt_automation
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
brew install poppler

python app.py


## 📦 API Endpoints

### 📤 POST `/upload`

Uploads a scanned receipt PDF.

**Form Data:**
- Key: `file` (PDF only)

**Response:**
```json
{ "message": "Uploaded", "id": 1 }
````

---

###  POST `/validate`

Validates whether the uploaded file is a valid PDF.

**Request:**

```json
{ "file_id": 1 }
```

**Response:**

```json
{ "is_valid": true, "reason": null }
```

---

### 🤖 POST `/process`

Extracts receipt data using Hugging Face's LayoutLM model.

**Request:**

```json
{ "file_id": 1 }
```

**Response:**

```json
{
  "message": "Processed",
  "receipt_id": 1
}
```

---

### 📄 GET `/receipts`

Lists all processed receipts.

**Response:**

```json
[
  {
    "id": 1,
    "merchant_name": "Starbucks",
    "total_amount": 215.00,
    "purchased_at": "2024-06-14"
  }
]
```

---

### 🔍 GET `/receipts/<id>`

Retrieves detailed receipt information by ID.

**Response:**

```json
{
  "id": 1,
  "merchant_name": "Starbucks",
  "total_amount": 215.00,
  "purchased_at": "2024-06-14",
  "file_path": "receipts/sample1.pdf"
}


## 👨‍💻 Author

*Mohammed Muzzammil*
*[muzzammilsilat56@gmail.com](muzzammilsilat56@gmail.com)*
[LinkedIn](https://www.linkedin.com/in/mohammed-muzzammil/)
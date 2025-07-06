from transformers import pipeline
from pdf2image import convert_from_path
from PIL import Image
import os

# Load model pipeline once at module level
qa_pipeline = pipeline("document-question-answering", model="impira/layoutlm-document-qa")

def convert_pdf_to_image(pdf_path):
    pages = convert_from_path(pdf_path, dpi=200)
    image_path = pdf_path.replace(".pdf", ".jpg")
    pages[0].save(image_path, "JPEG")
    return image_path

def extract_receipt_data_from_hf(pdf_path):
    image_path = convert_pdf_to_image(pdf_path)
    image = Image.open(image_path)

    # Ask model questions
    merchant = qa_pipeline(image, question="Who is the merchant?")[0]['answer']
    amount = qa_pipeline(image, question="What is the total amount?")[0]['answer']
    date = qa_pipeline(image, question="When was the purchase made?")[0]['answer']

    # Clean and return structured result
    try:
        clean_amount = float(amount.replace('$', '').strip()) if amount.replace('.', '', 1).isdigit() else 0.0
    except:
        clean_amount = 0.0

    return {
        'merchant_name': merchant.strip(),
        'total_amount': clean_amount,
        'purchased_at': date.strip()
    }

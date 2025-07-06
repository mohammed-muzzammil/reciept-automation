from app import app, db
from flask import request, jsonify
from models import ReceiptFile, Receipt
from ocr_utils import extract_receipt_data_from_hf
import os
from werkzeug.utils import secure_filename

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file or not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Invalid file'}), 400
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    entry = ReceiptFile(file_name=filename, file_path=path)
    db.session.add(entry)
    db.session.commit()
    return jsonify({'message': 'Uploaded', 'id': entry.id}), 201

@app.route('/validate', methods=['POST'])
def validate():
    file_id = request.json.get('file_id')
    entry = ReceiptFile.query.get(file_id)
    if not entry:
        return jsonify({'error': 'Not found'}), 404
    entry.is_valid = entry.file_path.endswith('.pdf')
    if not entry.is_valid:
        entry.invalid_reason = "File is not a PDF"
    db.session.commit()
    return jsonify({'is_valid': entry.is_valid, 'reason': entry.invalid_reason})

@app.route('/process', methods=['POST'])
def process():
    file_id = request.json.get('file_id')
    file_entry = ReceiptFile.query.get(file_id)
    if not file_entry or not file_entry.is_valid:
        return jsonify({'error': 'File not found or invalid'}), 400

    data = extract_receipt_data_from_hf(file_entry.file_path)

    receipt = Receipt(
        merchant_name=data['merchant_name'],
        total_amount=data['total_amount'],
        purchased_at=data['purchased_at'],
        file_path=file_entry.file_path
    )
    db.session.add(receipt)
    file_entry.is_processed = True
    db.session.commit()

    return jsonify({'message': 'Processed', 'receipt_id': receipt.id})

@app.route('/receipts', methods=['GET'])
def list_receipts():
    receipts = Receipt.query.all()
    return jsonify([{
        'id': r.id,
        'merchant_name': r.merchant_name,
        'total_amount': r.total_amount,
        'purchased_at': r.purchased_at
    } for r in receipts])

@app.route('/receipts/<int:rid>', methods=['GET'])
def get_receipt(rid):
    r = Receipt.query.get(rid)
    if not r:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({
        'id': r.id,
        'merchant_name': r.merchant_name,
        'total_amount': r.total_amount,
        'purchased_at': r.purchased_at,
        'file_path': r.file_path
    })

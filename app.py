import os
import time
from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from pdf_processor import extract_text_from_pdf, create_cleaned_pdf
from ai_cleaner import clean_text_for_tts

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def log_debug(message):
    if os.getenv("AI_CLEAN_DEBUG", "").strip().lower() in {"1", "true", "yes"}:
        print(f"[app] {message}")

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle PDF upload and processing"""
    try:
        request_started = time.perf_counter()
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        log_debug(f"Upload saved: {filename} size={os.path.getsize(input_path)} bytes")
        
        # Process the PDF
        # Step 1: Extract text from PDF
        step_started = time.perf_counter()
        extracted_text = extract_text_from_pdf(input_path)
        log_debug(f"Extracted text length={len(extracted_text)} in {time.perf_counter() - step_started:.2f}s")
        
        if not extracted_text or not extracted_text.strip():
            os.remove(input_path)
            return jsonify({'error': 'Could not extract text from PDF'}), 400
        
        # Step 2: Clean text using AI
        step_started = time.perf_counter()
        cleaned_text = clean_text_for_tts(extracted_text)
        log_debug(f"AI clean length={len(cleaned_text)} in {time.perf_counter() - step_started:.2f}s")
        
        # Step 3: Create new PDF with cleaned text
        output_filename = f"cleaned_{filename}"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        step_started = time.perf_counter()
        create_cleaned_pdf(cleaned_text, output_path)
        log_debug(f"PDF created size={os.path.getsize(output_path)} bytes in {time.perf_counter() - step_started:.2f}s")
        
        # Clean up input file
        os.remove(input_path)
        
        log_debug(f"Request completed in {time.perf_counter() - request_started:.2f}s")

        return jsonify({
            'success': True,
            'filename': output_filename
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download the processed PDF"""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)

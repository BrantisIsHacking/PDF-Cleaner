import os
import time
import uuid
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

# Global progress tracking
progress_state = {}

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
    session_id = str(uuid.uuid4())
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
        
        # Initialize progress tracking
        progress_state[session_id] = {'completed': 0, 'total': 0}
        
        def progress_callback(completed, total):
            progress_state[session_id] = {'completed': completed, 'total': total}
            log_debug(f"Progress: {completed}/{total} chunks")
        
        # Process the PDF
        # Step 1: Extract text from PDF
        step_started = time.perf_counter()
        extracted_text = extract_text_from_pdf(input_path)
        log_debug(f"Extracted text length={len(extracted_text)} in {time.perf_counter() - step_started:.2f}s")
        
        if not extracted_text or not extracted_text.strip():
            os.remove(input_path)
            progress_state.pop(session_id, None)
            return jsonify({'error': 'Could not extract text from PDF'}), 400
        
        # Step 2: Clean text using AI
        step_started = time.perf_counter()
        cleaned_text = clean_text_for_tts(extracted_text, progress_callback=progress_callback)
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
        
        # Keep progress state for 5 seconds so client can poll final status
        progress_state[session_id] = {'completed': progress_state[session_id]['total'], 
                                       'total': progress_state[session_id]['total'],
                                       'cleanup_time': time.time() + 5}

        return jsonify({
            'success': True,
            'filename': output_filename,
            'session_id': session_id
        })
    
    except Exception as e:
        # Keep error state briefly for polling
        if session_id in progress_state:
            progress_state[session_id]['cleanup_time'] = time.time() + 5
        return jsonify({'error': str(e)}), 500

@app.route('/progress/<session_id>')
def get_progress(session_id):
    """Get current processing progress for a session"""
    if session_id in progress_state:
        progress = progress_state[session_id]
        # Clean up old sessions
        if 'cleanup_time' in progress and time.time() > progress['cleanup_time']:
            progress_state.pop(session_id, None)
            return jsonify({'error': 'Session expired'}), 404
        
        if progress['total'] > 0:
            percent = (progress['completed'] / progress['total']) * 100
        else:
            percent = 0
        log_debug(f"Progress query for {session_id}: {progress['completed']}/{progress['total']} ({percent:.1f}%)")
        return jsonify({
            'completed': progress['completed'],
            'total': progress['total'],
            'percent': percent
        })
    return jsonify({'error': 'Session not found'}), 404

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

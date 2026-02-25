# PDF Text Cleaner for Text-to-Speech

A web application using OpenAI's API to clean and optimize PDF text for text-to-speech applications.

## Features

- AI-powered text cleaning (fixes line breaks, removes headers/footers, corrects spacing)
- Drag-and-drop PDF upload
- Download cleaned PDF
- Modern web interface

## Prerequisites

- Python 3.8+
- OpenAI API key

## Quick Start

1. Clone/download the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install: `pip install -r requirements.txt`
5. Create `.env` and add your OpenAI API key: `OPENAI_API_KEY=your_key_here`
6. Run: `python app.py`
7. Open: `http://localhost:5000`

## How It Works

1. Extract text from PDF (PyPDF2)
2. Clean with OpenAI's GPT-4o-mini
3. Generate new PDF (ReportLab)
4. Download cleaned PDF

## Troubleshooting

- **API key error**: Make sure `.env` file exists with correct `OPENAI_API_KEY`
- **PDF extraction fails**: Some scanned PDFs need OCR first
- **File upload fails**: Check file is valid PDF and under 16MB

## Security

- Never commit `.env` to version control
- Keep your API key secret
- Temporary files are deleted after processing

## License

MIT License

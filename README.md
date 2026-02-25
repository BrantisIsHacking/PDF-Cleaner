# PDF Text Cleaner for Text-to-Speech

A web application that uses AI to clean and optimize PDF text for text-to-speech applications. Upload a PDF, and get back a cleaned version with properly formatted text that's perfect for TTS editors.

## Features

- 📄 **PDF Upload**: Simple drag-and-drop or click-to-upload interface
- 🤖 **AI-Powered Cleaning**: Uses OpenAI's GPT to intelligently clean text
- 🔧 **Smart Processing**: 
  - Fixes broken line breaks and hyphenation
  - Removes page numbers, headers, and footers
  - Corrects spacing and punctuation
  - Removes artifacts and special characters
  - Maintains natural sentence flow
- 📥 **Download Cleaned PDF**: Get a new PDF with optimized text
- 💫 **Beautiful UI**: Modern, responsive web interface

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   - Copy `.env.example` to `.env`:
     ```bash
     copy .env.example .env
     ```
   - Edit `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     ```

## Getting an OpenAI API Key

1. Go to [OpenAI's website](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy the key and add it to your `.env` file

**Note**: The application uses GPT-4o-mini which is cost-effective. Check OpenAI's pricing for current rates.

## Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

3. **Upload a PDF**:
   - Click the upload area or drag and drop a PDF file
   - Wait for the AI to process and clean the text
   - Download your cleaned PDF

4. **Use the cleaned PDF** in your text-to-speech editor!

## How It Works

1. **Extract**: Extracts text from the uploaded PDF using PyPDF2
2. **Clean**: Sends the text to OpenAI's GPT-4o-mini to clean and optimize for TTS
3. **Generate**: Creates a new PDF with the cleaned text using ReportLab
4. **Download**: Provides the cleaned PDF for download

## File Structure

```
PDF-Cleaner/
├── app.py                 # Main Flask application
├── ai_cleaner.py          # AI text cleaning logic
├── pdf_processor.py       # PDF extraction and generation
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create from .env.example)
├── .env.example          # Example environment file
├── .gitignore            # Git ignore rules
├── templates/
│   └── index.html        # Web interface
└── uploads/              # Temporary file storage (created automatically)
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

### App Configuration

In `app.py`, you can modify:
- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 16MB)
- `UPLOAD_FOLDER`: Directory for temporary files (default: 'uploads')
- Port and host settings in `app.run()`

## Troubleshooting

### "OpenAI API key not found"
- Make sure you've created a `.env` file
- Verify your API key is correctly set in the `.env` file
- Restart the application after creating/editing `.env`

### "Could not extract text from PDF"
- Some PDFs may be scanned images without text
- Try a different PDF or use OCR software first

### File upload fails
- Check that the file is a valid PDF
- Ensure the file is under 16MB
- Verify you have write permissions in the project directory

## Security Notes

- Never commit your `.env` file to version control
- Keep your OpenAI API key secret
- The application creates temporary files that are deleted after processing
- Consider adding authentication for production use

## Cost Considerations

- Each PDF processing uses OpenAI API credits
- GPT-4o-mini is used for cost efficiency
- Monitor your API usage on the OpenAI dashboard
- Consider setting usage limits on your OpenAI account

## Future Enhancements

- Support for multiple file formats
- Batch processing
- Preview before download
- Custom cleaning rules
- Local AI models for offline processing
- User authentication
- Processing history

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Support

For issues, questions, or contributions, please open an issue on the project repository.

---

**Enjoy cleaner PDFs for your text-to-speech projects! 🎙️**

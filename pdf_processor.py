from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as a string
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
        
        return text.strip()
    
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def create_cleaned_pdf(text, output_path):
    """
    Create a new PDF with cleaned text optimized for text-to-speech
    
    Args:
        text: Cleaned text content
        output_path: Path where the PDF should be saved
    """
    try:
        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Create a custom style for the body text with spacing built-in
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=12,
            leading=16,
            alignment=TA_LEFT,
            spaceAfter=12
        )
        
        # Split text into paragraphs and build elements efficiently
        paragraphs = text.split('\n\n')
        
        for para_text in paragraphs:
            para_text = para_text.strip()
            if para_text:
                # Create paragraph object - spaceAfter handles spacing, no need for Spacer
                elements.append(Paragraph(para_text, body_style))
        
        # Build the PDF
        doc.build(elements)
        
        return True
    
    except Exception as e:
        raise Exception(f"Error creating PDF: {str(e)}")

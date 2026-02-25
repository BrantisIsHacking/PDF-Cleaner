import os
from openai import OpenAI

def clean_text_for_tts(text):
    """
    Use AI to clean and optimize text for text-to-speech applications
    
    This function:
    - Fixes formatting issues (broken line breaks, hyphenation)
    - Removes unnecessary symbols and artifacts
    - Improves readability for TTS
    - Maintains natural sentence structure
    
    Args:
        text: Raw text extracted from PDF
        
    Returns:
        Cleaned text optimized for TTS
    """
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            raise Exception("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file")
        
        client = OpenAI(api_key=api_key)
        
        # Create the prompt for text cleaning
        system_prompt = """You are a text cleaning assistant specialized in preparing text for text-to-speech applications.

Your tasks:
1. Fix broken line breaks and hyphenation (e.g., "exam-\nple" becomes "example")
2. Remove page numbers, headers, footers, and irrelevant metadata
3. Fix spacing and punctuation issues
4. Remove special characters that don't contribute to meaning
5. Ensure proper sentence structure and paragraph breaks
6. Preserve the original meaning and content
7. Make the text flow naturally for spoken reading
8. Keep abbreviations that are commonly spoken (e.g., Dr., Mr., etc.)

Return ONLY the cleaned text, with no explanations or additional comments."""

        user_prompt = f"""Please clean the following text extracted from a PDF so it can be used in a text-to-speech editor:

{text}"""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        
        cleaned_text = response.choices[0].message.content.strip()
        
        return cleaned_text
    
    except Exception as e:
        raise Exception(f"Error cleaning text with AI: {str(e)}")

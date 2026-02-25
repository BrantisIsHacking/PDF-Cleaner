import os
import time
import concurrent.futures
import google.generativeai as genai

def log_debug(message):
    if os.getenv("AI_CLEAN_DEBUG", "").strip().lower() in {"1", "true", "yes"}:
        print(f"[ai_cleaner] {message}")

def split_text_into_chunks(text, max_chars):
    if not text:
        return []

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""

    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}" if current else paragraph
        if len(candidate) <= max_chars:
            current = candidate
            continue

        if current:
            chunks.append(current)
            current = ""

        if len(paragraph) <= max_chars:
            current = paragraph
            continue

        start = 0
        while start < len(paragraph):
            end = start + max_chars
            chunks.append(paragraph[start:end])
            start = end

    if current:
        chunks.append(current)

    return chunks

def clean_text_for_tts(text):
    """
    Use Google Gemini AI to clean and optimize text for text-to-speech applications
    
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
        api_key = os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            raise Exception("Google API key not found. Please set GOOGLE_API_KEY in your .env file")
        
        genai.configure(api_key=api_key)
        
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

        # Call Google Gemini API with bounded waits and chunking to avoid hanging requests
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        timeout_seconds = int(os.getenv('AI_CLEAN_TIMEOUT_SECONDS', '120'))
        max_chunk_chars = int(os.getenv('AI_CLEAN_MAX_CHARS', '6000'))

        chunks = split_text_into_chunks(text, max_chunk_chars)
        if not chunks:
            return ""

        log_debug(f"Starting AI clean: chunks={len(chunks)}, max_chunk_chars={max_chunk_chars}")

        cleaned_chunks = []

        for index, chunk in enumerate(chunks, start=1):
            log_debug(f"Chunk {index}/{len(chunks)} size={len(chunk)} starting")
            chunk_prompt = f"""Please clean the following text extracted from a PDF so it can be used in a text-to-speech editor:

{chunk}"""

            def generate_response():
                return model.generate_content([system_prompt + "\n\n" + chunk_prompt])

            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(generate_response)
                try:
                    started = time.perf_counter()
                    response = future.result(timeout=timeout_seconds)
                    elapsed = time.perf_counter() - started
                    log_debug(f"Chunk {index}/{len(chunks)} completed in {elapsed:.2f}s")
                except concurrent.futures.TimeoutError:
                    log_debug(f"Chunk {index}/{len(chunks)} timed out after {timeout_seconds}s")
                    raise Exception("AI request timed out. Please try again or reduce PDF size.")

            cleaned_chunk = response.text.strip() if response and response.text else ""
            cleaned_chunks.append(cleaned_chunk)

        return "\n\n".join([c for c in cleaned_chunks if c])
    
    except Exception as e:
        raise Exception(f"Error cleaning text with AI: {str(e)}")

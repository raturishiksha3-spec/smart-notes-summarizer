import re
import string
from typing import List, Dict

def clean_text(text: str) -> str:
    """
    Clean and preprocess text for summarization
    
    Args:
        text: Raw text input
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s.,!?;:\-\'\"()]', '', text)
    
    # Fix spacing around punctuation
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    
    # Capitalize first letter of sentences
    text = '. '.join(sentence.capitalize() for sentence in text.split('. '))
    
    return text.strip()

def validate_text_length(text: str, min_words: int = 50, max_words: int = 10000) -> Dict[str, any]:
    """
    Validate text length for processing
    
    Args:
        text: Input text
        min_words: Minimum required words
        max_words: Maximum allowed words
        
    Returns:
        Dictionary with validation result
    """
    word_count = len(text.split())
    
    if word_count < min_words:
        return {
            "valid": False,
            "error": f"Text too short. Minimum {min_words} words required. You have {word_count} words.",
            "word_count": word_count
        }
    
    if word_count > max_words:
        return {
            "valid": False,
            "error": f"Text too long. Maximum {max_words} words allowed. You have {word_count} words.",
            "word_count": word_count
        }
    
    return {
        "valid": True,
        "word_count": word_count
    }

def extract_key_sentences(text: str, num_sentences: int = 3) -> List[str]:
    """
    Extract key sentences from text using simple heuristics
    
    Args:
        text: Input text
        num_sentences: Number of sentences to extract
        
    Returns:
        List of key sentences
    """
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if len(sentences) <= num_sentences:
        return sentences
    
    # Score sentences by length and position
    scored_sentences = []
    for idx, sentence in enumerate(sentences):
        # Early sentences get higher scores
        position_score = 1.0 / (idx + 1)
        # Longer sentences get higher scores (up to a point)
        length_score = min(len(sentence.split()) / 20, 1.0)
        total_score = position_score * 0.6 + length_score * 0.4
        scored_sentences.append((sentence, total_score))
    
    # Sort by score and take top N
    scored_sentences.sort(key=lambda x: x[1], reverse=True)
    return [s[0] for s in scored_sentences[:num_sentences]]

def format_summary_as_bullets(summary: str) -> str:
    """
    Convert paragraph summary to bullet points
    
    Args:
        summary: Summary text
        
    Returns:
        Formatted bullet points
    """
    sentences = re.split(r'[.!?]+', summary)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    
    bullets = ['• ' + sentence + '.' for sentence in sentences]
    return '\n'.join(bullets)

def truncate_text(text: str, max_chars: int = 500) -> str:
    """
    Truncate text to specified character limit
    
    Args:
        text: Input text
        max_chars: Maximum characters
        
    Returns:
        Truncated text
    """
    if len(text) <= max_chars:
        return text
    
    # Try to cut at sentence boundary
    truncated = text[:max_chars]
    last_period = truncated.rfind('.')
    
    if last_period > max_chars * 0.8:
        return truncated[:last_period + 1]
    
    return truncated + '...'

def calculate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """
    Calculate estimated reading time in minutes
    
    Args:
        text: Input text
        words_per_minute: Average reading speed
        
    Returns:
        Reading time in minutes
    """
    word_count = len(text.split())
    return max(1, round(word_count / words_per_minute))

def extract_document_metadata(text: str) -> Dict[str, any]:
    """
    Extract basic metadata from document
    
    Args:
        text: Document text
        
    Returns:
        Dictionary with metadata
    """
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    paragraphs = text.split('\n\n')
    
    return {
        "word_count": len(words),
        "sentence_count": len([s for s in sentences if s.strip()]),
        "paragraph_count": len([p for p in paragraphs if p.strip()]),
        "reading_time_minutes": calculate_reading_time(text),
        "character_count": len(text),
        "avg_word_length": sum(len(word) for word in words) / len(words) if words else 0,
        "avg_sentence_length": len(words) / len([s for s in sentences if s.strip()]) if sentences else 0
    }

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe storage
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove path components
    filename = filename.split('/')[-1].split('\\')[-1]
    
    # Remove or replace invalid characters
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    filename = ''.join(c for c in filename if c in valid_chars)
    
    # Limit length
    name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
    if len(name) > 50:
        name = name[:50]
    
    return f"{name}.{ext}" if ext else name

def merge_summaries(summaries: List[str]) -> str:
    """
    Merge multiple chunk summaries into coherent text
    
    Args:
        summaries: List of summary chunks
        
    Returns:
        Merged summary
    """
    if not summaries:
        return ""
    
    if len(summaries) == 1:
        return summaries[0]
    
    # Remove redundant information
    merged = []
    seen_sentences = set()
    
    for summary in summaries:
        sentences = re.split(r'[.!?]+', summary)
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and sentence.lower() not in seen_sentences:
                seen_sentences.add(sentence.lower())
                merged.append(sentence)
    
    return '. '.join(merged) + '.'

def generate_title_from_text(text: str, max_length: int = 50) -> str:
    """
    Generate a title from text content
    
    Args:
        text: Input text
        max_length: Maximum title length
        
    Returns:
        Generated title
    """
    # Extract first sentence or first N words
    first_sentence = text.split('.')[0].strip()
    
    if len(first_sentence) <= max_length:
        return first_sentence
    
    # Take first N words
    words = first_sentence.split()
    title = ' '.join(words[:8])
    
    if len(title) > max_length:
        title = title[:max_length - 3] + '...'
    
    return title
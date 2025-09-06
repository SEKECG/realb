import re
from token_encoder import get_token_length

def split_text_into_sentences(text, parent_text=None, chunk_size=500):
    """
    Split a given text into sentences or chunks of specified size, optionally prepending a parent text to each chunk, 
    while ensuring minimal token overlap and handling short texts appropriately.
    
    Args:
        text: The text to split into sentences/chunks.
        parent_text: Optional parent text to prepend to each chunk.
        chunk_size: Maximum token size for each chunk.
        
    Returns:
        List[str]: List of text chunks.
    """
    if not text:
        return []
    
    # Split text into sentences using common sentence delimiters
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = []
    current_token_count = 0
    
    # If parent_text is provided, calculate its token length
    parent_token_length = get_token_length(parent_text) if parent_text else 0
    
    for sentence in sentences:
        sentence_token_length = get_token_length(sentence)
        
        # Check if adding this sentence would exceed chunk size
        if current_token_count + sentence_token_length + parent_token_length > chunk_size:
            if current_chunk:
                # Join current chunk and add to results
                chunk_text = " ".join(current_chunk)
                if parent_text:
                    chunk_text = parent_text + " " + chunk_text
                chunks.append(chunk_text)
                
                # Reset current chunk
                current_chunk = [sentence]
                current_token_count = sentence_token_length
            else:
                # Single sentence is too long, split it further
                if sentence_token_length > chunk_size - parent_token_length:
                    # Split long sentence into smaller parts
                    words = sentence.split()
                    temp_chunk = []
                    temp_token_count = 0
                    
                    for word in words:
                        word_token_length = get_token_length(word)
                        
                        if temp_token_count + word_token_length > chunk_size - parent_token_length:
                            if temp_chunk:
                                chunk_text = " ".join(temp_chunk)
                                if parent_text:
                                    chunk_text = parent_text + " " + chunk_text
                                chunks.append(chunk_text)
                            
                            temp_chunk = [word]
                            temp_token_count = word_token_length
                        else:
                            temp_chunk.append(word)
                            temp_token_count += word_token_length
                    
                    if temp_chunk:
                        chunk_text = " ".join(temp_chunk)
                        if parent_text:
                            chunk_text = parent_text + " " + chunk_text
                        chunks.append(chunk_text)
                else:
                    # Add single sentence as chunk
                    chunk_text = sentence
                    if parent_text:
                        chunk_text = parent_text + " " + chunk_text
                    chunks.append(chunk_text)
        else:
            current_chunk.append(sentence)
            current_token_count += sentence_token_length
    
    # Add the last chunk if it exists
    if current_chunk:
        chunk_text = " ".join(current_chunk)
        if parent_text:
            chunk_text = parent_text + " " + chunk_text
        chunks.append(chunk_text)
    
    return chunks
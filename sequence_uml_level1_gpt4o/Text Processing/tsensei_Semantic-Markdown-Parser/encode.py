import os
from pathlib import Path
from transformers import AutoTokenizer

current_dir = Path(__file__).parent
tokenizer_path = current_dir / "tokenizer"
tokenizer = None

def get_tokens(content):
    """
    Tokenize the input string content into a list of tokens using a predefined tokenizer.
    
    Args:
        content: The text content to tokenize.
        
    Returns:
        list: List of tokens.
    """
    global tokenizer
    if tokenizer is None:
        if tokenizer_path.exists() and tokenizer_path.is_dir():
            tokenizer = AutoTokenizer.from_pretrained(str(tokenizer_path))
        else:
            # Fallback to a default tokenizer if custom one not found
            tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    
    if not content:
        return []
    
    return tokenizer.encode(content, add_special_tokens=False)

def get_token_length(content):
    """
    Calculate the number of tokens in a given string using a tokenizer.
    
    Args:
        content: The text content to calculate token length for.
        
    Returns:
        int: Number of tokens in the content.
    """
    tokens = get_tokens(content)
    return len(tokens)
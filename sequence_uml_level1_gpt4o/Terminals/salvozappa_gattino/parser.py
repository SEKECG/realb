proj_clean/src/parser.py
import re


def extract_first_code_block(text):
    """
    Extract the first code block enclosed in triple backticks (```) from a given text string, removing any 'bash' specifier if present, and return the content of the code block as a stripped string. If no code block is found, return an empty string.
    """
    pattern = r'```(?:bash)?\s*(.*?)```'
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        code_block = match.group(1).strip()
        return code_block
    return ""
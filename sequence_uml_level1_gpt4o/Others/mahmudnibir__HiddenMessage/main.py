import base64
import os
import time
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from PIL import Image

# Constants
AUTHOR_NAME = "Mahmud Nibir"
AUTHOR_GITHUB = "https://github.com/mahmudnibir"
AUTHOR_PROJECT = "HiddenMessage"
IMAGE_PATH = "input_image.png"
OUTPUT_IMAGE_PATH = "output_image.png"
PASSWORD = "mysecretpassword"

def animated_logo(text):
    """Prints the logo with a typing animation effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.05)
    print()

def print_AUTHOR_info():
    """Display the author's information in a stylized manner."""
    print("\n" + "="*50)
    print(f"Author: {AUTHOR_NAME}")
    print(f"GitHub: {AUTHOR_GITHUB}")
    print(f"Project: {AUTHOR_PROJECT}")
    print("="*50 + "\n")

def generate_key(password):
    """Generate encryption key from password"""
    password_bytes = password.encode()
    salt = b'salt_'  # Fixed salt for simplicity (in real use, should be random)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    return key

def encrypt_text(text, password):
    """Encrypt text using AES"""
    key = generate_key(password)
    fernet = Fernet(key)
    encrypted_text = fernet.encrypt(text.encode())
    return base64.urlsafe_b64encode(encrypted_text).decode()

def decrypt_text(encrypted_text, password):
    """Decrypt text using AES"""
    try:
        key = generate_key(password)
        fernet = Fernet(key)
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_text.encode())
        decrypted_text = fernet.decrypt(encrypted_bytes)
        return decrypted_text.decode()
    except Exception as e:
        return f"Decryption failed: {str(e)}"

def text_to_bin(text):
    """Convert text to binary"""
    return ''.join(format(ord(char), '08b') for char in text)

def bin_to_text(binary_data):
    """Convert binary to text"""
    text = ''
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if len(byte) == 8:
            text += chr(int(byte, 2))
    return text

def hide_text_in_image(IMAGE_PATH, text, OUTPUT_IMAGE_PATH, password):
    """Hide encrypted text inside an image"""
    try:
        # Encrypt the text
        encrypted_text = encrypt_text(text, password)
        
        # Convert to binary
        binary_data = text_to_bin(encrypted_text)
        binary_data += '1111111111111110'  # End of message marker
        
        # Open the image
        image = Image.open(IMAGE_PATH)
        pixels = image.load()
        width, height = image.size
        
        # Check if image can hold the message
        max_bits = width * height * 3
        if len(binary_data) > max_bits:
            return f"Message too large for image. Max bits: {max_bits}, Needed: {len(binary_data)}"
        
        data_index = 0
        
        # Embed the binary data in the LSB of RGB channels
        for y in range(height):
            for x in range(width):
                if data_index >= len(binary_data):
                    break
                
                r, g, b = pixels[x, y][:3]
                
                # Modify red channel
                if data_index < len(binary_data):
                    r = (r & 0xFE) | int(binary_data[data_index])
                    data_index += 1
                
                # Modify green channel
                if data_index < len(binary_data):
                    g = (g & 0xFE) | int(binary_data[data_index])
                    data_index += 1
                
                # Modify blue channel
                if data_index < len(binary_data):
                    b = (b & 0xFE) | int(binary_data[data_index])
                    data_index += 1
                
                pixels[x, y] = (r, g, b)
        
        # Save the modified image
        image.save(OUTPUT_IMAGE_PATH)
        return f"Text hidden successfully in {OUTPUT_IMAGE_PATH}"
        
    except Exception as e:
        return f"Error hiding text: {str(e)}"

def extract_text_from_image(IMAGE_PATH, password):
    """Extract encrypted text from an image"""
    try:
        # Open the image
        image = Image.open(IMAGE_PATH)
        pixels = image.load()
        width, height = image.size
        
        binary_data = ""
        
        # Extract LSB from RGB channels
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y][:3]
                
                # Extract from red channel
                binary_data += str(r & 1)
                
                # Extract from green channel
                binary_data += str(g & 1)
                
                # Extract from blue channel
                binary_data += str(b & 1)
        
        # Find the end of message marker
        end_marker = binary_data.find('1111111111111110')
        if end_marker != -1:
            binary_data = binary_data[:end_marker]
        
        # Convert binary to text
        encrypted_text = bin_to_text(binary_data)
        
        # Decrypt the text
        decrypted_text = decrypt_text(encrypted_text, password)
        
        return decrypted_text
        
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def main():
    """Main function to run the steganography application"""
    animated_logo("=== Hidden Message - LSB Steganography with AES ===")
    print_AUTHOR_info()
    
    while True:
        print("\nMenu:")
        print("1. Hide text in image")
        print("2. Extract text from image")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            image_path = input("Enter input image path (or press Enter for default): ").strip()
            if not image_path:
                image_path = IMAGE_PATH
            
            output_path = input("Enter output image path (or press Enter for default): ").strip()
            if not output_path:
                output_path = OUTPUT_IMAGE_PATH
            
            password = input("Enter password (or press Enter for default): ").strip()
            if not password:
                password = PASSWORD
            
            text = input("Enter text to hide: ").strip()
            
            result = hide_text_in_image(image_path, text, output_path, password)
            print(result)
            
        elif choice == "2":
            image_path = input("Enter image path to extract from (or press Enter for default): ").strip()
            if not image_path:
                image_path = OUTPUT_IMAGE_PATH
            
            password = input("Enter password (or press Enter for default): ").strip()
            if not password:
                password = PASSWORD
            
            extracted_text = extract_text_from_image(image_path, password)
            print(f"Extracted text: {extracted_text}")
            
        elif choice == "3":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
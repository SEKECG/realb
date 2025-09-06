import hashlib
import zlib
import base64
import mimetypes
import os
import glob
from emoji_codec import EmojiCodec, CompressionMethod, VerificationMethod
from emojichef_cli import Colors

def get_valid_input(prompt, valid_options):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        print(f"Invalid option. Valid options are: {', '.join(valid_options)}")

def handle_batch_processing(codec):
    file_pattern = input("Enter file pattern (e.g., *.txt): ").strip()
    output_dir = input("Enter output directory: ").strip()
    operation = get_valid_input("Enter operation (encode/decode): ", ["encode", "decode"])
    codec.batch_process(file_pattern, output_dir, operation)

def handle_file_operations(codec):
    input_path = input("Enter input file path: ").strip()
    output_path = input("Enter output file path: ").strip()
    operation = get_valid_input("Enter operation (encode/decode): ", ["encode", "decode"])
    codec.process_file(input_path, output_path, operation)

def handle_quick_operation(codec):
    operation = get_valid_input("Enter operation (encode/decode): ", ["encode", "decode"])
    data = input("Enter text to process: ").strip()
    if operation == "encode":
        print(codec.encode(data))
    else:
        print(codec.decode(data))

def handle_settings(codec):
    recipe_type = get_valid_input("Enter recipe type (quick/light/classic/gourmet): ", ["quick", "light", "classic", "gourmet"])
    compression = get_valid_input("Enable compression (yes/no): ", ["yes", "no"])
    verification = get_valid_input("Enable verification (yes/no): ", ["yes", "no"])
    codec.recipe_type = recipe_type
    codec.compression = CompressionMethod.ZLIB if compression == "yes" else CompressionMethod.NONE
    codec.verification = VerificationMethod.SHA256 if verification == "yes" else VerificationMethod.NONE
    return codec

def print_banner():
    print(f"{Colors.BOLD}{Colors.HEADER}Welcome to EmojiChef!{Colors.ENDC}")

def print_menu():
    print(f"{Colors.BOLD}{Colors.BLUE}Main Menu:{Colors.ENDC}")
    print("1. Quick Encode/Decode")
    print("2. File Operations")
    print("3. Batch Processing")
    print("4. Settings")
    print("5. View Recipe Book")
    print("6. Exit")

def view_recipe_book():
    print(f"{Colors.BOLD}{Colors.GREEN}Recipe Book:{Colors.ENDC}")
    print("Quick (Base-64): Uses food emojis (🍅🍆🍇)")
    print("Light (Base-128): Uses activity emojis (🎰🎱🎲)")
    print("Classic (Base-256): Uses smiley emojis (😀😃😄)")
    print("Gourmet (Base-1024): Uses extended emoji set (🤠🤡🤢)")

def main():
    codec = EmojiCodec(recipe_type="quick", compression=CompressionMethod.NONE, verification=VerificationMethod.NONE)
    print_banner()
    while True:
        print_menu()
        choice = get_valid_input("Choose an option: ", ["1", "2", "3", "4", "5", "6"])
        if choice == "1":
            handle_quick_operation(codec)
        elif choice == "2":
            handle_file_operations(codec)
        elif choice == "3":
            handle_batch_processing(codec)
        elif choice == "4":
            codec = handle_settings(codec)
        elif choice == "5":
            view_recipe_book()
        elif choice == "6":
            print("Exiting EmojiChef. Goodbye!")
            break

if __name__ == "__main__":
    main()
import argparse
from emojichef import handle_batch_processing, handle_file_operations, handle_quick_operation, handle_settings
from emoji_codec import EmojiCodec

__version__ = "1.0.0"

class Colors:
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
    GREEN = '\033[92m'
    HEADER = '\033[95m'
    RED = '\033[91m'
    YELLOW = '\033[93m'

class EmojiChefCLI:
    def __init__(self):
        self.parser = self._create_parser()
        self.use_color = True

    def _create_parser(self):
        parser = argparse.ArgumentParser(description="EmojiChef CLI")
        parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
        parser.add_argument('--color', action='store_true', help="Enable color output")
        parser.add_argument('--no-color', action='store_true', help="Disable color output")
        subparsers = parser.add_subparsers(dest='command')

        encode_parser = subparsers.add_parser('encode', help="Encode text or file")
        encode_parser.add_argument('input', help="Input text or file path")
        encode_parser.add_argument('--output', help="Output file path")
        encode_parser.add_argument('--recipe', choices=['quick', 'light', 'classic', 'gourmet'], default='quick', help="Encoding recipe")
        encode_parser.add_argument('--compress', action='store_true', help="Enable compression")
        encode_parser.add_argument('--verify', choices=['none', 'sha256'], default='none', help="Verification method")

        decode_parser = subparsers.add_parser('decode', help="Decode emoji text or file")
        decode_parser.add_argument('input', help="Input emoji text or file path")
        decode_parser.add_argument('--output', help="Output file path")

        batch_parser = subparsers.add_parser('batch', help="Batch process files")
        batch_parser.add_argument('pattern', help="File pattern to match")
        batch_parser.add_argument('output_dir', help="Output directory")
        batch_parser.add_argument('--operation', choices=['encode', 'decode'], required=True, help="Operation to perform")
        batch_parser.add_argument('--recipe', choices=['quick', 'light', 'classic', 'gourmet'], default='quick', help="Encoding recipe")
        batch_parser.add_argument('--compress', action='store_true', help="Enable compression")
        batch_parser.add_argument('--verify', choices=['none', 'sha256'], default='none', help="Verification method")

        return parser

    def analyze_input(self, input_path, codec):
        file_info = codec.get_file_info(input_path)
        print(f"File Info: {file_info}")
        suggested_recipe = codec._suggest_recipe(file_info['size'])
        print(f"Suggested Recipe: {suggested_recipe}")

    def batch_process(self, pattern, output_dir, codec, operation, quiet):
        results = codec.batch_process(pattern, output_dir, operation)
        if not quiet:
            for result in results:
                print(f"Processed: {result['file']} -> {result['output']}")

    def colorize(self, text, color):
        if self.use_color:
            return f"{color}{text}{Colors.ENDC}"
        return text

    def process_file(self, input_path, output_path, codec, operation, quiet):
        result = codec.process_file(input_path, output_path, operation)
        if not quiet:
            print(f"Processed: {result['file']} -> {result['output']}")

    def process_text(self, text, codec, operation, quiet):
        if operation == 'encode':
            result = codec.encode(text)
        else:
            result = codec.decode(text)
        if not quiet:
            print(f"Result: {result}")
        return result

    def run(self):
        args = self.parser.parse_args()
        if args.color:
            self.use_color = True
        if args.no_color:
            self.use_color = False

        codec = handle_settings(EmojiCodec(args.recipe, args.compress, args.verify))

        if args.command == 'encode':
            if args.output:
                self.process_file(args.input, args.output, codec, 'encode', False)
            else:
                self.process_text(args.input, codec, 'encode', False)
        elif args.command == 'decode':
            if args.output:
                self.process_file(args.input, args.output, codec, 'decode', False)
            else:
                self.process_text(args.input, codec, 'decode', False)
        elif args.command == 'batch':
            self.batch_process(args.pattern, args.output_dir, codec, args.operation, False)

def main():
    cli = EmojiChefCLI()
    cli.run()

if __name__ == "__main__":
    main()
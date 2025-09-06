import argparse
import json
from crx_analyzer.extension import Extension, InvalidExtensionIDError
from crx_analyzer.risk import get_risk_report
from crx_analyzer.download import download_extension, get_chrome_extension_url, get_edge_extension_url

def analyze(id, browser, output, max_files, max_urls, permissions):
    try:
        with Extension(id, browser, '.') as ext:
            risk_report = get_risk_report(ext)
            if output == 'json':
                print(json.dumps(risk_report, indent=4))
            else:
                print(f"Extension Name: {ext.name}")
                print(f"Version: {ext.version}")
                print(f"Author: {ext.author}")
                print(f"Permissions: {ext.permissions}")
                print(f"JavaScript Files: {ext.javascript_files[:max_files]}")
                print(f"Referenced URLs: {ext.urls[:max_urls]}")
                print(f"Risk Score: {risk_report['risk_score']}")
                print(f"Risk Levels: {risk_report['risk_levels']}")
    except InvalidExtensionIDError:
        print(f"Invalid extension ID: {id}")

def get_version():
    print("Chrome/Edge Extension Analyzer v1.0")

def cli():
    parser = argparse.ArgumentParser(description="Chrome/Edge Extension Analyzer")
    subparsers = parser.add_subparsers(dest='command')

    version_parser = subparsers.add_parser('version', help='Show the tool version')
    version_parser.set_defaults(func=get_version)

    analyze_parser = subparsers.add_parser('analyze', help='Perform extension analysis')
    analyze_parser.add_argument('id', help='Extension ID')
    analyze_parser.add_argument('browser', choices=['chrome', 'edge'], help='Browser type')
    analyze_parser.add_argument('--output', choices=['pretty', 'json'], default='pretty', help='Output format')
    analyze_parser.add_argument('--max_files', type=int, default=10, help='Max JavaScript files to display')
    analyze_parser.add_argument('--max_urls', type=int, default=10, help='Max URLs to display')
    analyze_parser.add_argument('--permissions', action='store_true', help='Show only permissions and metadata')
    analyze_parser.set_defaults(func=analyze)

    args = parser.parse_args()
    if args.command:
        args.func(**vars(args))

if __name__ == "__main__":
    cli()
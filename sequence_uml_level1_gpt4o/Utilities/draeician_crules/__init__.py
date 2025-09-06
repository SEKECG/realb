#!/usr/bin/env python3
"""
CLI interface for generating Cursor rules files.
"""

import argparse
import logging
import sys
from pathlib import Path

from . import __version__
from .config import load_config
from .cursor_ops import CursorDirectoryManager
from .file_ops import (
    backup_existing_rules,
    check_files_exist,
    combine_rules,
    copy_predefined_rules,
    list_available_languages,
    setup_directory_structure,
    update_gitignore,
    write_rules_to_cursor_dir,
)

logger = logging.getLogger(__name__)


def main(languages=None, force=False, verbose=False, show_list=False, setup_dirs=False, legacy=False):
    """
    Generate cursor rules files.
    
    By default, creates individual rule files in .cursor/rules directory.
    Use --legacy to generate a single .cursorrules file instead.
    
    Use --setup to initialize or update the rules directory structure.
    Use --force with --setup to update existing rule files.
    Use --list to see available language rules.
    Use --verbose for detailed operation logging.
    """
    try:
        config = load_config()
        
        if verbose:
            logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
            logger.info("Verbose mode enabled")
        
        cursor_manager = CursorDirectoryManager(config)
        
        if show_list:
            list_available_languages(config['language_rules_dir'])
            return
        
        if setup_dirs:
            success = setup_directory_structure(verbose, force)
            if success:
                print("Directory structure setup completed successfully.")
            else:
                print("Directory structure setup failed.")
            return
        
        cursor_manager.ensure_cursor_structure()
        
        if not check_files_exist(config['global_rules'], config['language_rules_dir'], languages):
            print("Required files are missing. Run with --setup to initialize the directory structure.")
            sys.exit(1)
        
        if legacy:
            backup_existing_rules(force)
            
            combined_rules = combine_rules(
                config['global_rules'],
                config['language_rules_dir'],
                languages,
                config['delimiter']
            )
            
            with open('.cursorrules', 'w', encoding='utf-8') as f:
                f.write(combined_rules)
            
            update_gitignore()
            print("Generated .cursorrules file in legacy mode.")
        else:
            success = write_rules_to_cursor_dir(
                cursor_manager,
                config['global_rules'],
                config['language_rules_dir'],
                languages,
                force
            )
            
            if success:
                cursor_manager.update_gitignore()
                print("Generated rule files in .cursor/rules/ directory.")
            else:
                print("Failed to generate rule files.")
                sys.exit(1)
    
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Cursor rules files")
    parser.add_argument('languages', nargs='*', help='Language identifiers for rules (e.g., python, javascript)')
    parser.add_argument('--force', '-f', action='store_true', help='Force overwrite existing files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--list', '-l', action='store_true', dest='show_list', help='List available language rules')
    parser.add_argument('--setup', '-s', action='store_true', dest='setup_dirs', help='Setup directory structure')
    parser.add_argument('--legacy', action='store_true', help='Generate single .cursorrules file instead of multiple files')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    args = parser.parse_args()
    
    main(
        languages=args.languages,
        force=args.force,
        verbose=args.verbose,
        show_list=args.show_list,
        setup_dirs=args.setup_dirs,
        legacy=args.legacy
    )
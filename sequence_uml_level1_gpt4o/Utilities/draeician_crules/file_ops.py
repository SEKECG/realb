"""
File operations for managing rule files.
"""

import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)


def setup_directory_structure(verbose, force):
    """
    Create necessary directories and files for crules.
    
    Args:
        verbose: Whether to show verbose output
        force: Whether to overwrite existing files
    """
    try:
        if verbose:
            logger.info("Setting up directory structure...")
        
        # Create language_rules directory
        lang_rules_dir = Path('language_rules')
        lang_rules_dir.mkdir(exist_ok=True)
        
        if verbose:
            logger.info(f"Created language_rules directory: {lang_rules_dir}")
        
        # Copy predefined rules
        copy_predefined_rules(lang_rules_dir, verbose, force)
        
        # Create global rules file if it doesn't exist
        global_rules = Path('global_rules.mdc')
        if not global_rules.exists() or force:
            global_rules.write_text("# Global rules\n\nAdd your global rules here.", encoding='utf-8')
            if verbose:
                logger.info(f"Created global rules file: {global_rules}")
        
        # Create config file if it doesn't exist
        config_file = Path('crules_config.yaml')
        if not config_file.exists() or force:
            config_content = """# crules configuration
global_rules: global_rules.mdc
language_rules_dir: language_rules
delimiter: "---"
"""
            config_file.write_text(config_content, encoding='utf-8')
            if verbose:
                logger.info(f"Created config file: {config_file}")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to setup directory structure: {e}")
        return False


def list_available_languages(language_rules_dir):
    """
    Display all available language rule files.
    """
    try:
        available_languages = get_available_languages(language_rules_dir)
        
        if not available_languages:
            print("No language rules found. Run with --setup to initialize.")
            return
        
        print("Available language rules:")
        for lang_name, lang_path in available_languages.items():
            print(f"  - {lang_name}")
            
    except Exception as e:
        logger.error(f"Failed to list available languages: {e}")


def check_files_exist(global_rules, language_rules_dir, languages):
    """
    Check if all required files exist.
    """
    try:
        # Check global rules
        global_rules_path = Path(global_rules)
        if not global_rules_path.exists():
            logger.warning(f"Global rules file not found: {global_rules}")
            return False
        
        # Check language rules directory
        lang_rules_dir_path = Path(language_rules_dir)
        if not lang_rules_dir_path.exists():
            logger.warning(f"Language rules directory not found: {language_rules_dir}")
            return False
        
        # If specific languages are requested, check they exist
        if languages:
            available_languages = get_available_languages(language_rules_dir)
            for lang in languages:
                if lang not in available_languages:
                    logger.warning(f"Language rule not found: {lang}")
                    return False
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to check files existence: {e}")
        return False


def backup_existing_rules(force):
    """
    Backup existing .cursorrules file if it exists.
    """
    try:
        cursorrules_path = Path('.cursorrules')
        backup_path = Path('.cursorrules.bak')
        
        if cursorrules_path.exists():
            if backup_path.exists() and not force:
                logger.warning("Backup file already exists. Use --force to overwrite.")
                return False
            
            shutil.copy2(cursorrules_path, backup_path)
            logger.info(f"Backed up existing .cursorrules to {backup_path}")
            return True
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to backup existing rules: {e}")
        return False


def combine_rules(global_rules, language_rules_dir, languages, delimiter):
    """
    Combine global and language-specific rules.
    """
    try:
        combined_content = []
        
        # Add global rules
        global_rules_path = Path(global_rules)
        if global_rules_path.exists():
            combined_content.append(global_rules_path.read_text(encoding='utf-8'))
        
        # Add language-specific rules
        if languages:
            available_languages = get_available_languages(language_rules_dir)
            for lang in languages:
                if lang in available_languages:
                    lang_content = available_languages[lang].read_text(encoding='utf-8')
                    combined_content.append(lang_content)
        
        return f"\n{delimiter}\n".join(combined_content)
        
    except Exception as e:
        logger.error(f"Failed to combine rules: {e}")
        return ""


def write_rules_to_cursor_dir(cursor_manager, global_rules, lang_rules_dir, languages, force):
    """
    Write rules to the .cursor/rules directory.
    
    Args:
        cursor_manager: Instance of CursorDirectoryManager
        global_rules: Path to global rules file
        lang_rules_dir: Path to language rules directory
        languages: List of language identifiers
        force: Whether to force overwrite existing files
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Write global rules
        global_rules_path = Path(global_rules)
        if global_rules_path.exists():
            global_content = global_rules_path.read_text(encoding='utf-8')
            success = cursor_manager.create_rule_file("global", global_content)
            if not success:
                return False
        
        # Write language-specific rules
        if languages:
            available_languages = get_available_languages(lang_rules_dir)
            for lang in languages:
                if lang in available_languages:
                    lang_content = available_languages[lang].read_text(encoding='utf-8')
                    success = cursor_manager.create_rule_file(lang, lang_content)
                    if not success:
                        return False
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to write rules to cursor directory: {e}")
        return False


def copy_predefined_rules(lang_rules_dir, verbose, force):
    """
    Copy predefined language rules to the lang_rules directory.
    """
    try:
        # This would typically copy from a package directory
        # For now, we'll create some example files
        predefined_rules = {
            'python': "# Python rules\n\nAdd your Python-specific rules here.",
            'javascript': "# JavaScript rules\n\nAdd your JavaScript-specific rules here.",
            'typescript': "# TypeScript rules\n\nAdd your TypeScript-specific rules here.",
            'java': "# Java rules\n\nAdd your Java-specific rules here.",
            'go': "# Go rules\n\nAdd your Go-specific rules here.",
        }
        
        for lang_name, rule_content in predefined_rules.items():
            rule_file = lang_rules_dir / f"{lang_name}.mdc"
            
            if not rule_file.exists() or force:
                rule_file.write_text(rule_content, encoding='utf-8')
                if verbose:
                    logger.info(f"Created rule file: {rule_file}")
                    
    except Exception as e:
        logger.error(f"Failed to copy predefined rules: {e}")


def get_available_languages(language_rules_dir):
    """
    Get all available language rule files.
    """
    try:
        lang_rules_dir_path = Path(language_rules_dir)
        
        if not lang_rules_dir_path.exists():
            return {}
        
        language_files = {}
        for rule_file in lang_rules_dir_path.glob('*.mdc'):
            language_files[rule_file.stem] = rule_file
        
        return language_files
        
    except Exception as e:
        logger.error(f"Failed to get available languages: {e}")
        return {}


def update_gitignore():
    """
    Add .cursorrules and .cursorrules.bak to .gitignore if it exists.
    """
    try:
        gitignore_path = Path('.gitignore')
        patterns = ['.cursorrules', '.cursorrules.bak']
        
        if not gitignore_path.exists():
            return
        
        content = gitignore_path.read_text(encoding='utf-8')
        
        for pattern in patterns:
            if pattern not in content:
                if content.strip() and not content.endswith('\n'):
                    content += '\n'
                content += f"{pattern}\n"
        
        gitignore_path.write_text(content, encoding='utf-8')
        logger.info("Updated .gitignore to include cursor rules backup files")
        
    except Exception as e:
        logger.error(f"Failed to update .gitignore: {e}")
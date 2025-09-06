"""
Cursor directory operations for managing .cursor/rules structure.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class CursorDirectoryManager:
    """Manages the .cursor directory structure and rule files."""
    
    def __init__(self, config):
        """
        Initialize the cursor directory manager.
        
        Args:
            config: Configuration dictionary containing paths and settings
        """
        self.config = config
        self.cursor_dir = Path('.cursor')
        self.rules_dir = self.cursor_dir / 'rules'
    
    def create_rule_file(self, name, content, metadata=None):
        """
        Create a rule file with optional metadata.
        
        Args:
            name: Name of the rule file (without extension)
            content: Rule content
            metadata: Optional metadata dictionary
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.ensure_cursor_structure()
            
            file_path = self.rules_dir / f"{name}.mdc"
            
            if metadata:
                metadata_content = "\n".join([f"{k}: {v}" for k, v in metadata.items()])
                full_content = f"{metadata_content}\n\n{content}"
            else:
                full_content = content
            
            file_path.write_text(full_content, encoding='utf-8')
            logger.info(f"Created rule file: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create rule file {name}: {e}")
            return False
    
    def ensure_cursor_structure(self):
        """Create the .cursor directory structure if it doesn't exist."""
        try:
            self.rules_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Ensured cursor directory structure exists at {self.rules_dir}")
        except Exception as e:
            logger.error(f"Failed to create cursor directory structure: {e}")
            raise
    
    def list_rule_files(self):
        """
        List all rule files in the .cursor/rules directory.
        
        Returns:
            List[Path]: List of paths to rule files
        """
        try:
            if not self.rules_dir.exists():
                return []
            
            rule_files = list(self.rules_dir.glob('*.mdc'))
            return rule_files
            
        except Exception as e:
            logger.error(f"Failed to list rule files: {e}")
            return []
    
    def update_gitignore(self):
        """Update .gitignore to include .cursor/rules/*.mdc."""
        try:
            gitignore_path = Path('.gitignore')
            pattern = '.cursor/rules/*.mdc'
            
            if not gitignore_path.exists():
                gitignore_path.write_text(f"# Cursor rules files\n{pattern}\n", encoding='utf-8')
                logger.info("Created .gitignore with cursor rules pattern")
                return
            
            content = gitignore_path.read_text(encoding='utf-8')
            
            if pattern not in content:
                if content.strip() and not content.endswith('\n'):
                    content += '\n'
                content += f"# Cursor rules files\n{pattern}\n"
                gitignore_path.write_text(content, encoding='utf-8')
                logger.info("Updated .gitignore to include cursor rules pattern")
                
        except Exception as e:
            logger.error(f"Failed to update .gitignore: {e}")
"""
Configuration management for crules.
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict

import yaml

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    'global_rules': 'global_rules.mdc',
    'language_rules_dir': 'language_rules',
    'delimiter': '---'
}


def load_config() -> Dict[str, Any]:
    """
    Load configuration from YAML file or return defaults.
    
    Returns:
        Dict[str, Any]: Configuration dictionary with all settings
    """
    config_file = Path('crules_config.yaml')
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
            
            # Merge with defaults, allowing user config to override defaults
            final_config = DEFAULT_CONFIG.copy()
            final_config.update(config)
            return final_config
            
        except Exception as e:
            logger.warning(f"Failed to load config file: {e}. Using default configuration.")
            return DEFAULT_CONFIG.copy()
    else:
        return DEFAULT_CONFIG.copy()
proj_clean/src/config.py
import json
import os


def load_config():
    """
    Load and parse a JSON configuration file located at '~/.config/kitty/gattino/gattino.config.json', 
    returning its contents as a dictionary. If the file is not found or contains invalid JSON, 
    return an empty dictionary and print an appropriate error message.
    """
    config_path = os.path.expanduser('~/.config/kitty/gattino/gattino.config.json')
    
    try:
        with open(config_path, 'r') as config_file:
            config_data = json.load(config_file)
        return config_data
    except FileNotFoundError:
        print(f"Configuration file not found at: {config_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in configuration file: {e}")
        return {}
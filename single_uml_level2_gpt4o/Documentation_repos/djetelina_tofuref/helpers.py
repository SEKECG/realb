import os
import json
import re
import logging
from pathlib import Path
from datetime import datetime, timedelta
import requests

CODEBLOCK_REGEX = re.compile(r'```(.*?)```', re.DOTALL)
LOGGER = logging.getLogger(__name__)
jsonlib = json

def cached_file_path(endpoint):
    return Path(f"cache/{endpoint.replace('/', '_')}")

def get_from_cache(endpoint):
    cache_path = cached_file_path(endpoint)
    if cache_path.exists():
        with open(cache_path, 'r') as file:
            return file.read()
    return None

def get_registry_api(endpoint, json=True, log_widget=None, timeout=10):
    cache_content = get_from_cache(endpoint)
    if cache_content:
        if json:
            return jsonlib.loads(cache_content)
        return cache_content

    response = requests.get(f"https://registry.opentofu.com/{endpoint}", timeout=timeout)
    if log_widget:
        log_widget.log(f"GET {endpoint} - {response.status_code}")
    
    if response.status_code == 200:
        save_to_cache(endpoint, response.text)
        if json:
            return response.json()
        return response.text
    return None

def header_markdown_split(contents):
    if contents.startswith("---"):
        header_end = contents.find("---", 3)
        if header_end != -1:
            header = contents[:header_end+3]
            body = contents[header_end+3:]
            return jsonlib.loads(header), body
    return {}, contents

def is_provider_index_expired(file, timeout=31):
    if not file.exists():
        return True
    file_time = datetime.fromtimestamp(file.stat().st_mtime)
    return datetime.now() - file_time > timedelta(days=timeout)

def save_to_cache(endpoint, contents):
    cache_path = cached_file_path(endpoint)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_path, 'w') as file:
        file.write(contents)
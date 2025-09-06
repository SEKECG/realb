import os
import tempfile
import subprocess
import json
import threading
from typing import List, Dict, Any, Optional

CODE_FILES_FIELD = "code_files"
CONFIG_FIELD = "config"
DEFAULT_TIMEOUT = 300  # 5 mins in seconds
RULE_FIELD = "rule"
RULE_ID_FIELD = "rule_id"
SEMGREP_API_URL = "https://semgrep.dev/api"
SEMGREP_URL = "https://semgrep.dev"
__version__ = "0.2.1"
_semgrep_lock = threading.Lock()
http_client = None
semgrep_executable: Optional[str] = None

class McpError(Exception):
    pass

class CodeFile:
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content

class CodeWithLanguage:
    def __init__(self, content, language="python"):
        self.content = content
        self.language = language

class SemgrepScanResult:
    def __init__(self, version, results, errors, paths, skipped_rules):
        self.version = version
        self.results = results
        self.errors = errors
        self.paths = paths
        self.skipped_rules = skipped_rules

def main(transport=None):
    if transport == "stdio":
        # Implement stdio transport logic
        pass
    elif transport == "sse":
        # Implement SSE transport logic
        pass
    else:
        raise McpError("Unsupported transport")

def create_temp_files_from_code_content(code_files):
    try:
        temp_dir = tempfile.mkdtemp()
        for code_file in code_files:
            file_path = os.path.join(temp_dir, code_file.filename)
            with open(file_path, 'w') as f:
                f.write(code_file.content)
        return temp_dir
    except Exception as e:
        raise McpError(f"Error creating temp files: {e}")

def ensure_semgrep_available():
    global semgrep_executable
    with _semgrep_lock:
        if semgrep_executable is None:
            semgrep_executable = find_semgrep_path()
            if semgrep_executable is None:
                raise McpError("Semgrep not found")
    return semgrep_executable

def find_semgrep_path():
    common_paths = ["/usr/local/bin/semgrep", "/usr/bin/semgrep"]
    for path in common_paths:
        if os.path.exists(path):
            return path
    return None

def get_abstract_syntax_tree(code, language):
    # Implement AST generation logic
    pass

def get_semgrep_rule_schema():
    # Implement rule schema retrieval logic
    pass

def get_semgrep_rule_yaml(rule_id):
    # Implement rule YAML retrieval logic
    pass

def get_semgrep_scan_args(temp_dir, config=None):
    args = [ensure_semgrep_available(), "scan", "--json", "--config", config or "auto", temp_dir]
    return args

def get_supported_languages():
    # Implement supported languages retrieval logic
    pass

def remove_temp_dir_from_results(results, temp_dir):
    # Implement results cleaning logic
    pass

def run_semgrep(args):
    try:
        result = subprocess.run(args, capture_output=True, timeout=DEFAULT_TIMEOUT)
        return result.stdout.decode('utf-8')
    except subprocess.TimeoutExpired:
        raise McpError("Semgrep scan timed out")

def safe_join(base_dir, untrusted_path):
    final_path = os.path.abspath(os.path.join(base_dir, untrusted_path))
    if not final_path.startswith(base_dir):
        raise McpError("Unsafe path detected")
    return final_path

def security_check(code_files):
    # Implement security check logic
    pass

def semgrep_rule_schema():
    # Implement rule schema retrieval logic
    pass

def semgrep_scan(code_files, config=None):
    temp_dir = create_temp_files_from_code_content(code_files)
    args = get_semgrep_scan_args(temp_dir, config)
    output = run_semgrep(args)
    results = json.loads(output)
    remove_temp_dir_from_results(results, temp_dir)
    return SemgrepScanResult(
        version=results.get("version"),
        results=results.get("results"),
        errors=results.get("errors"),
        paths=results.get("paths"),
        skipped_rules=results.get("skipped_rules")
    )

def semgrep_scan_with_custom_rule(code_files, rule):
    temp_dir = create_temp_files_from_code_content(code_files)
    rule_path = os.path.join(temp_dir, "custom_rule.yaml")
    with open(rule_path, 'w') as f:
        f.write(rule)
    args = get_semgrep_scan_args(temp_dir, rule_path)
    output = run_semgrep(args)
    results = json.loads(output)
    remove_temp_dir_from_results(results, temp_dir)
    return SemgrepScanResult(
        version=results.get("version"),
        results=results.get("results"),
        errors=results.get("errors"),
        paths=results.get("paths"),
        skipped_rules=results.get("skipped_rules")
    )

def validate_absolute_path(path_to_validate, param_name):
    if not os.path.isabs(path_to_validate):
        raise McpError(f"{param_name} must be an absolute path")
    return path_to_validate

def validate_code_files(code_files):
    if not isinstance(code_files, list) or not all(isinstance(cf, CodeFile) for cf in code_files):
        raise McpError("Invalid code_files parameter")

def validate_config(config):
    if config and not isinstance(config, str):
        raise McpError("Invalid config parameter")
    return config

def write_custom_semgrep_rule(code, language):
    # Implement custom rule writing logic
    pass
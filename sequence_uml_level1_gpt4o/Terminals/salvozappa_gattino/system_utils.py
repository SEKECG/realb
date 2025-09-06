proj_clean/src/system_utils.py
import subprocess
import threading
import time
from ui import Spinner


def run_command(command, input=None):
    """
    Execute a shell command with optional input, display a spinner during execution, and return the command's output while handling errors.
    """
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE if input else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        spinner = Spinner()
        spinner_thread = threading.Thread(target=spinner.show, args=(process,))
        spinner_thread.start()
        
        stdout, stderr = process.communicate(input=input)
        return_code = process.wait()
        
        spinner_thread.join()
        
        if return_code != 0:
            return f"Error: {stderr.strip()}"
        
        return stdout.strip()
        
    except Exception as e:
        return f"Exception occurred: {str(e)}"


def write_file(path, content):
    """
    Write content to a file at the specified path.
    """
    try:
        with open(path, 'w') as file:
            file.write(content)
    except Exception as e:
        print(f"Error writing to file {path}: {str(e)}")
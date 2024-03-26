import os
from datetime import datetime
from tzlocal import get_localzone
import sys

def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_application_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(__file__)

def log(filename, data):
    # Get the base directory of the script or the executable
    application_path = get_application_path()
    
    # Specify the path to the 'output' directory relative to the application path
    output_dir = os.path.join(application_path, 'output')
    
    # Ensure the 'output' directory exists
    ensure_dir_exists(output_dir)
    
    # Specify the path to the file within the 'output' directory
    file_path = os.path.join(output_dir, filename)
    
    # Get the current timestamp in the local timezone
    timestamp = datetime.now(tz=get_localzone())
    data["timestamp"] = timestamp.isoformat()
    
    # Safely open the file for appending and write the data
    with open(file_path, 'a', encoding="utf-8") as log:
        log.write(f"{data}\n")



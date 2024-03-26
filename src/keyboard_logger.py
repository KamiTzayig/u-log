import time
from pynput import keyboard

import os
from datetime import datetime
from tzlocal import get_localzone
import sys
import json

def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_desktop_path():
    # For Windows
    if os.name == 'nt':
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    # For MacOS
    elif os.name == 'posix':
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    # Adjust as needed for other operating systems
    else:
        raise NotImplementedError("This script only supports Windows and MacOS.")
    return desktop

def log(filename, data):
    # Specify the path to the 'output' directory on the Desktop
    output_dir = os.path.join(get_desktop_path(), 'u-log/output'+datetime.today().strftime('%Y%m%d'))
    
    # Ensure the 'output' directory exists
    ensure_dir_exists(output_dir)
    
    # Specify the path to the file within the 'output' directory
    file_path = os.path.join(output_dir, filename)
    
    # Get the current timestamp in the local timezone
    timestamp = datetime.now(tz=get_localzone())
    data["timestamp"] = timestamp.isoformat()
    
        # Serialize data to a JSON string if it's a dictionary
    if isinstance(data, dict):
        data_str = json.dumps(data, ensure_ascii=False)
    else:
        data_str = str(data)
    
    # Safely open the file for appending and write the data
    with open(file_path, 'a', encoding="utf-8") as log:
        log.write(f"{data_str}\n")





def logKey(key, is_pressed):
    if type(key) == keyboard.KeyCode:
        id = key.vk
        value = key.char,
        is_dead = key.is_dead,
        combining = key.combining
    elif type(key) == keyboard.Key:
        id = key.value.vk
        value = key.name
        is_dead = (False,)
        combining = None
    else:
        print("error")
        

    d = {
        "id": id,
        "value": value,
        "is_pressed": is_pressed,
        "is_dead": is_dead,
        "combining": combining,
    }

    try:
        log("keyboard_logs.txt", d)
            
    except Exception as e:
        print("Error getting char")
        print(e)


def keyPressed(key):
    logKey(key, True)
   
def keyReleased(key):
    logKey(key, False)

listener = keyboard.Listener(on_press=keyPressed, on_release=keyReleased)
listener.start()

while True:
    time.sleep(1)



import copy
import time
from pynput import mouse
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


def on_move(x, y):
    d["position"] = (x, y)

    log("mouse_logs.txt", d)

def on_click(x, y, button, pressed):
    if button == mouse.Button.left:
        d["button_left"] = pressed
    elif button == mouse.Button.right:
        d["button_right"] = pressed
    elif button == mouse.Button.middle:
        d["button_middle"] = pressed
    d["position"] = (x, y)
    log("mouse_logs.txt", d)

def on_scroll(x, y, dx, dy):
    d["position"] = (x, y)
    scroll_dict = copy.deepcopy(d)
    if dy < 0:
        scroll_dict["scroll_down"] = True
    else:
        scroll_dict["scroll_up"] = True

    log("mouse_logs.txt", scroll_dict)


d ={
    "timestamp": time.time(),
    "position": (0,0),
    "button_left": False,
    "button_right": False,
    "button_middle": False,
    "scroll_up": False,
    "scroll_down": False,
}
log("mouse_logs.txt", d)


listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
listener.start()
input("Press Enter to stop...\n")

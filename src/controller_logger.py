import os
import time
import pygame
import json  
from datetime import datetime
from tzlocal import get_localzone


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





pygame.init()
joysticks = []
clock = pygame.time.Clock()
INTERVAL = 0.2
last_time = time.time()

for i in range(0, pygame.joystick.get_count()):
    # create an Joystick object in our list
    joysticks.append(pygame.joystick.Joystick(i))
    # initialize the appended joystick (-1 means last array item)
    joysticks[-1].init()
    
    print ("Detected joystick "),joysticks[-1].get_name(),"'"
while True:
    clock.tick(60)
    for event in pygame.event.get():
        d = event.__dict__.copy()
        d["type"] = str(pygame.event.event_name(event.type))
        if d["type"] == "JoyAxisMotion":
            if time.time() - last_time >= INTERVAL:
                last_time = time.time()
                log("controller_logs.txt", d)
        else:
            log("controller_logs.txt", d)

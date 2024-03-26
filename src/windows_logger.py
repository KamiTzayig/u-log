import pywinctl as pwc
import time

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
    

    # Safely open the file for appending and write the data
    with open(file_path, 'a', encoding="utf-8") as log:
        log.write(f"{data}\n")



class WindowLogger:

    def __init__(self, window) -> None:
        self.window = window
        self.d = {
            "window_id": window._hWnd,
            "title": window.title,
            "size": window.size,
            "position": window.position,
            "is_alive": window.isAlive,
            "is_active": window.isActive,
            "is_visible": window.isVisible,
            "is_minimized": window.isMinimized,
            "is_maximized": window.isMaximized,
        }

        log("window_logs.txt", self.d)


    def event_log(self, key, value):
        self.d[key] = value
        log("window_logs.txt", self.d)
            


    # Callback for when the window is no longer alive
    def isAliveCB(self, alive):
        self.event_log("is_alive", alive)
        existing_windows_id_list.remove(self.window._hWnd)# Remove the window from the list of known windows

    # Callback for active status change
    def isActiveCB(self, active):
        self.event_log("is_active", active)

    # Callback for visible status change
    def isVisibleCB(self, visible):
        self.event_log("is_visible", visible)

    # Callback for minimized status change
    def isMinimizedCB(self, minimized):
        self.event_log("is_minimized", minimized)

    # Callback for maximized status change
    def isMaximizedCB(self, maximized):
        self.event_log("is_maximized", maximized)

    # Callback for window resize
    def resizedCB(self, size):
        self.event_log("size", size)

    # Callback for window movement
    def movedCB(self, pos):
        self.event_log("position", pos)

    # Callback for title change
    def changedTitleCB(self, title):
        self.event_log("title", title)

    # Callback for display change
    def changedDisplayCB(self, display):
        self.event_log("display", display)



    def start_watchdog(self):
        self.window.watchdog.start(
            isAliveCB = self.isAliveCB,
            isActiveCB = self.isActiveCB,
            isVisibleCB = self.isVisibleCB,
            isMinimizedCB = self.isMinimizedCB,
            isMaximizedCB = self.isMaximizedCB,
            resizedCB = self.resizedCB,
            movedCB = self.movedCB,
            changedTitleCB = self.changedTitleCB,
            changedDisplayCB = self.changedDisplayCB
        )




existing_windows_id_list = []

def monitor_new_windows():
    all_windows = pwc.getAllWindows()
    new_windows = [w for w in all_windows if w.title and w._hWnd not in existing_windows_id_list]

    for w in new_windows:
        window_logger = WindowLogger(w)
        window_logger.start_watchdog()
        existing_windows_id_list.append(w._hWnd)

while True:
    monitor_new_windows()
    time.sleep(1)

import pywinctl as pwc
import time


class WindowLogger:

    def __init__(self, window) -> None:
        self.window = window
        self.d = {
            "window_id": window._hWnd,
            # "appname": window.getAppName(),
            "title": window.title,
            "size": window.size,
            "position": window.position,
            "is_alive": window.isAlive,
            "is_active": window.isActive,
            "is_visible": window.isVisible,
            "is_minimized": window.isMinimized,
            "is_maximized": window.isMaximized,
            # "display": window.getDisplay()[0],
            "timestamp": time.time(),
            "created_time": time.time(),
        }

        with open("windowsfile.txt", 'a', encoding="utf-8") as windowsfile:
            windowsfile.write(f"{self.d}\n")  

    def log(self, key, value):
        timestamp = time.time()
        self.d[key] = value
        self.d["timestamp"] = timestamp
            
        with open("windowsfile.txt", 'a', encoding="utf-8") as windowsfile:
            windowsfile.write(f"{self.d}\n")  
            


    # Callback for when the window is no longer alive
    def isAliveCB(self, alive):
        self.log("is_alive", alive)
        existing_windows_id_list.remove(self.window._hWnd)# Remove the window from the list of known windows

    # Callback for active status change
    def isActiveCB(self, active):
        self.log("is_active", active)

    # Callback for visible status change
    def isVisibleCB(self, visible):
        self.log("is_visible", visible)

    # Callback for minimized status change
    def isMinimizedCB(self, minimized):
        self.log("is_minimized", minimized)

    # Callback for maximized status change
    def isMaximizedCB(self, maximized):
        self.log("is_maximized", maximized)

    # Callback for window resize
    def resizedCB(self, size):
        self.log("size", size)

    # Callback for window movement
    def movedCB(self, pos):
        self.log("position", pos)

    # Callback for title change
    def changedTitleCB(self, title):
        self.log("title", title)

    # Callback for display change
    def changedDisplayCB(self, display):
        self.log("display", display)



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

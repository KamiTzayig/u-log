import copy
import time
from pynput import mouse

def on_move(x, y):
    timestamp = time.time()
    d["timestamp"] = timestamp
    d["position"] = (x, y)

    with open("mousefile.txt", 'a', encoding="utf-8") as logMouse:
        logMouse.write(f"{d}\n")

def on_click(x, y, button, pressed):
    timestamp = time.time ()  
    d["timestamp"] = timestamp
    if button == mouse.Button.left:
        d["button_left"] = pressed
    elif button == mouse.Button.right:
        d["button_right"] = pressed
    elif button == mouse.Button.middle:
        d["button_middle"] = pressed
    d["position"] = (x, y)
    with open("mousefile.txt", 'a', encoding="utf-8") as logMouse:
        logMouse.write(f"{d}\n")

def on_scroll(x, y, dx, dy):
    timestamp = time.time ()  
    d["timestamp"] = timestamp
    d["position"] = (x, y)
    scroll_dict = copy.deepcopy(d)
    if dy < 0:
        scroll_dict["scroll_down"] = True
    else:
        scroll_dict["scroll_up"] = True

    with open("mousefile.txt", 'a', encoding="utf-8") as logMouse:
        logMouse.write(f"{scroll_dict}\n")


d ={
    "timestamp": time.time(),
    "position": (0,0),
    "button_left": False,
    "button_right": False,
    "button_middle": False,
    "scroll_up": False,
    "scroll_down": False,
}
with open("mousefile.txt", 'a', encoding="utf-8") as logMouse:
        logMouse.write(f"{d}\n")

listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
listener.start()
input("Press Enter to stop...\n")

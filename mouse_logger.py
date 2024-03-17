import time
from pynput import mouse

def on_move(x, y):
    current_time = time.time()  # Capture the current timestamp
    with open("mousefile.txt", 'a') as logMouse:
        logMouse.write(f"{current_time} Movement Position: {x}, {y}\n")  # Log the timestamp and mouse position

def on_click(x, y, button, pressed):
    current_time = time.time()  # Capture the current timestamp
    action = 'Pressed' if pressed else 'Released'
    with open("mousefile.txt", 'a') as logMouse:
        logMouse.write(f"{current_time} Click - {action} {button} at Position: {x}, {y}\n")  # Log the click

if __name__ == "__main__":
    # Set up a listener for mouse movements and clicks
    listener = mouse.Listener(on_move=on_move, on_click=on_click)
    listener.start()
    input("Press Enter to stop...\n")

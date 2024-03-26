
import pygame
import sys
import json  # For better formatting of the logged data

def log(left_analog_x, left_analog_y, right_analog_x, right_analog_y, a_button, b_button, x_button, y_button):
    d = {
        "Left Analog": {"X": left_analog_x, "Y": left_analog_y},
        "Right Analog": {"X": right_analog_x, "Y": right_analog_y},
        "Buttons": {"A": a_button, "B": b_button, "X": x_button, "Y": y_button}
    }

    with open("xbox_controller.txt", 'a', encoding="utf-8") as log_xbox_controller:
        try:
            # Using json.dumps for better readability in the log file
            log_xbox_controller.write(f"{json.dumps(d)}\n")
        except Exception: 
            print("Error logging controller data")
# Initialize Pygame
pygame.init()

# Initialize the joystick module
pygame.joystick.init()

# Try to setup an Xbox controller
try:
    xbox_controller = pygame.joystick.Joystick(0)  # Assumes the Xbox controller is the first one connected
    xbox_controller.init()
except pygame.error:
    print("Failed to connect to the Xbox controller")
    sys.exit()
    

try:
    # Assuming you have already initialized pygame and the controller
    while True:
        # Your event polling loop here...

        # Example of getting controller state (this should be in your event polling loop)
        left_analog_x = xbox_controller.get_axis(0)
        left_analog_y = xbox_controller.get_axis(1)
        right_analog_x = xbox_controller.get_axis(4)
        right_analog_y = xbox_controller.get_axis(3)
        a_button = xbox_controller.get_button(0)
        b_button = xbox_controller.get_button(1)
        x_button = xbox_controller.get_button(2)
        y_button = xbox_controller.get_button(3)

        # Log the current state
        log(left_analog_x, left_analog_y, right_analog_x, right_analog_y, a_button, b_button, x_button, y_button)

        pygame.time.wait(100)  # Delay to make the output readable, adjust as needed
except KeyboardInterrupt:
    print("Program exited by user.")
    pygame.quit()

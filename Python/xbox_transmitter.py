import pygame
import sys
import serial
import time

# Connect to esp32
esp32 = serial.Serial('COM6', 115200, timeout=1)
time.sleep(0.2)  # Allow esp32 to reset

# Initialize pygame and joystick module
pygame.init()
pygame.joystick.init()

# Check for at least one joystick
if pygame.joystick.get_count() == 0:
    print("No joystick detected. Please connect a controller.")
    sys.exit()

# Initialize the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Initialized Controller: {joystick.get_name()}")

values = [0,0,0,0]
offsets = [0,0,0,0]  # To store initial offsets for calibration

# Main loop
j=0
while True:
    # Handle events (required for pygame to work properly)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Read axis values (usually 0–3 are left/right stick x/y)
    axis_values = []
    for i in range(4):  # Read first 4 axes
        axis = joystick.get_axis(i)
        axis_values.append(axis)
    
    axis_values[1] = -axis_values[1]  # Invert Y-axis for left stick
    axis_values[3] = -axis_values[3]  # Invert Y-axis for right stick

    # print(j)
    if(j==0):
        offsets = axis_values
        j += 1
        continue

    values[0] = (axis_values[0]-offsets[0])*45
    values[1] = (axis_values[2]-offsets[2])*30
    values[2] = (axis_values[3]-offsets[3])*30
    values[3] = (axis_values[1]-offsets[1])

    str=""
    for value in values:
        str += f"{value} "
    str += "\n"
    esp32.write(str.encode('utf-8'))  # Send values to esp32
    time.sleep(0.05)  # Give esp32 time to process
    print(values)

    j += 1

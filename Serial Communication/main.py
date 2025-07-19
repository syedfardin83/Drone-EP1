import serial
import time

# Connect to Arduino
arduino = serial.Serial('COM6', 115200, timeout=1)
time.sleep(0.2)  # Allow Arduino to reset

# Send command
arduino.write(b"Hello there\n")
time.sleep(0.1)  # Give Arduino time to respond

# Read response
# if arduino.in_waiting:
#     response = arduino.readline().decode().strip()
#     print("Arduino:", response)

arduino.close()

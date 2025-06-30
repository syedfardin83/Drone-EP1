import serial
import time

# Connect to Arduino
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # Allow Arduino to reset

# Send command
arduino.write(b"TURN_OFF_LED\n")
time.sleep(0.1)  # Give Arduino time to respond

# Read response
if arduino.in_waiting:
    response = arduino.readline().decode().strip()
    print("Arduino:", response)

arduino.close()

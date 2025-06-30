import serial
import time

arduino = serial.Serial('COM3',9600)
time.sleep(2)

command = "100\n"

arduino.write(b"1\n")
time.sleep(0.1)  # Give Arduino time to respond

# Read response
if arduino.in_waiting:
    response = arduino.readline().decode().strip()
    print("Arduino:", response)

arduino.close()
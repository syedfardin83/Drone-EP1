import serial
import time

# Initialize serial connection
arduino = serial.Serial('COM3', 9600, timeout=1)  # Replace 'COM3' with your port
time.sleep(2)  # Wait for Arduino to initialize

try:
    while True:
        user_input = input("Enter data to send: ")  # User types a message
        arduino.write(f"{user_input}\n".encode())  # Send with newline

except KeyboardInterrupt:
    print("Closing...")
    arduino.close()
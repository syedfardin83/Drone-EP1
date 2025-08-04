import serial
import time

esp32 = serial.Serial('COM5', 115200, timeout=1)
time.sleep(0.1)  # Small delay to avoid overwhelming the ESP32

while True:
    inp = input("Enter command for ESP32 (or 'exit' to quit): ")
    if inp.lower() == 'exit':
        break
    inp+='\n'  # Append newline for ESP32 to recognize command
    esp32.write(inp.encode('utf-8'))  # Initialize Bluetooth on ESP32
    print(f"Sending: {inp.strip()}")

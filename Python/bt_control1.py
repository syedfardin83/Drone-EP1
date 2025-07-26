import serial
import time

esp32 = serial.Serial('COM6', 115200, timeout=1)
time.sleep(0.1)  # Small delay to avoid overwhelming the ESP32

esp32.write(b'HI THERE!!\n')  # Initialize Bluetooth on ESP32
esp32.close()  # Close the serial connection


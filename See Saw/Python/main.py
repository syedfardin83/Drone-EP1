import serial
import time

arduino = serial.Serial('COM3',9600)
time.sleep(2)

# arduino.write("0 0\n".encode())

while True:
    inp = input(">")
    if(inp=='exit'):
        print("# Exiting...")
        arduino.close()
        exit()
    arduino.write((inp+"\n").encode())
    time.sleep(0.1)
    if arduino.in_waiting:
        response = arduino.readline().decode().strip()
        print("# "+response)
import serial

mpu = serial.Serial('COM3',115200)

while True:
    line = mpu.readline().decode('utf-8')
    print(line)
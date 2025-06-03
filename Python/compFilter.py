import serial
import math

mpu = serial.Serial('COM3',115200)
line1 = mpu.readline().decode('utf-8')

def getSerialData():
    line = mpu.readline().decode('utf-8')
    try:
        a = line.strip().split(',')
    except:
        return []
    b=[]
    for i in a:
        try:
            b.append(float(i))
        except Exception as e:
            print(e)
            pass
    return b

#orient = 0 if ax is g
#orient = 1 if ay is g
#orient = 2 if az is g

def getAccPitch(data,orient):
    if orient==3:
        if data[2]==0:
            return math.pi/2
        return math.atan(data[0]/data[2]) 
    if orient==1:
        if data[0]==0:
            print('Perp')
            return math.pi/2
        return math.atan(data[2]/data[0])
    
while True:
    print(f'Pitch angle = {math.degrees(getAccPitch(getSerialData(),1))}')
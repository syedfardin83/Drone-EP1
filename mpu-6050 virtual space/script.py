import serial
from datetime import datetime
import pyautogui

mpu = serial.Serial('COM3',115200)
line = mpu.readline().decode('utf-8')
# this function returns an array
def getData():
    line = mpu.readline().decode('utf-8')

    a = line.strip().split(',')
    b=[]
    for i in a:
        try:
            b.append(float(i))
        except Exception as e:
            print(e)
            pass
    return b

def caliberateSensor():
    print('Caliberating sensor, make sure your sensor is at rest...')
    data = getData()
    offsetax=data[0]
    offsetay=data[1]
    offsetaz=data[2]
    offsetgx=data[3]
    offsetgy=data[4]
    offsetgz=data[5]
    print('Caliberation done!')

    return [offsetax,offsetay,offsetaz,offsetgx,offsetgy,offsetgz]

def getFilteredData(n):
    i=1
    sumax=0
    sumay=0
    sumaz=0
    sumgx=0
    sumgy=0
    sumgz=0
    while(i<=n):
        data=getData()
        sumax+=data[0]
        sumay+=data[1]
        sumaz+=data[2]
        sumgx+=data[3]
        sumgy+=data[4]
        sumgz+=data[5]
        i+=1
    avgax=sumax/n
    avgay=sumay/n
    avgaz=sumaz/n
    avggx=sumgx/n
    avggy=sumgy/n
    avggz=sumgz/n

    return [avgax,avgay,avgaz,avggx,avggy,avggz]
    
offsets = caliberateSensor()

s=200

while True:
    data = getFilteredData(10)
    # print(round(data[1]-offsets[1],1))

    x,y = pyautogui.position()

    pyautogui.moveTo(x-s*round(data[2]-offsets[2],1),y-s*round(data[1]-offsets[1],1))
    # print(f'Moving x to {x-s*round(data[2]-offsets[2],1)}')

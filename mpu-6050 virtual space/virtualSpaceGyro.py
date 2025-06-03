import serial
import time
import math

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
    

z=0
vx=0
ax=0
last_time = 0
offsets = caliberateSensor()

while True:
    data = getFilteredData(5)
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time

    # PROPER EULER INTEGRATION
    # # data = getFilteredData(5)
    # ax=round(data[3],1)
    # # ay=data[1]
    # # az=round(data[2]-round(offsets[2],1),1)
    # vx=vx+ax
    # x=x+vx
    # # print(z)
    # print(vx)
    # print(round(az-round(offsets[2],1),1))
    # print(az)

    # gyro y data
    z+=(data[4]-offsets[4])*dt
    print(f'Angle is {math.degrees(z)}')
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

def getFilteredData(n):
    i=1
    sumax=0
    sumay=0
    sumaz=0
    sumgx=0
    sumgy=0
    sumgz=0
    while(i<=n):
        data=getSerialData()
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

def caliberateSensor():
    print('Caliberating sensor, make sure your sensor is at rest...')
    data = getSerialData()
    offsetax=data[0]
    offsetay=data[1]
    offsetaz=data[2]
    offsetgx=data[3]
    offsetgy=data[4]
    offsetgz=data[5]

    return [offsetax,offsetay,offsetaz,offsetgx,offsetgy,offsetgz]

#orient = 1 if ax is g
#orient = 2 if ay is g
#orient = 3 if az is g

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

offsets = caliberateSensor()
last_time = 0
while True:
    #first acc data
    data = getFilteredData(5)
    accAngle = getAccPitch(data,1)
    print(accAngle)
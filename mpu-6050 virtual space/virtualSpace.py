#virtual space in z coord:

import serial

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
    
def caliberateSensor():
    print('Caliberating sensor, make sure your sensor is at rest...')
    data = getFilteredData(10)
    offsetax=data[0]
    offsetay=data[1]
    offsetaz=data[2]
    offsetgx=data[3]
    offsetgy=data[4]
    offsetgz=data[5]

    return [offsetax,offsetay,offsetaz,offsetgx,offsetgy,offsetgz]


z=0
vz=0
az=0
offsets = caliberateSensor()
while True:
    data = getFilteredData(10)
    ax=data[0]
    ay=data[1]
    az=round(data[2]-round(offsets[2],1),1)

    vz=round(vz+az,1)
    z=z+vz

    # print(z)
    print(vz)
    # print(round(az-round(offsets[2],1),1))
    # print(az)
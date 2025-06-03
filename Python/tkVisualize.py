import tkinter as tk
import serial
import math
import threading
import time

class App:
    def __init__(self,root):
        self.root = root

        self.mpu = serial.Serial('COM3',115200)
        line1 = self.mpu.readline().decode('utf-8')
        self.data = []

        self.orient = 1

        self.alpha = 0.98

        self.x11 = 100
        self.y11  = 100
        self.len1 = 100
        self.color1 = 'blue'
        self.width1 =  2

        self.x12 = 300
        self.y12  = 100
        self.len2 = 100
        self.color2 = 'green'
        self.width2 =  2

        self.x13 = 600
        self.y13  = 100
        self.len3 = 100
        self.color3 = 'red'
        self.width3 =  2

        self.accAngle = 0
        self.gyroAngle = 0

        self.buil_ui()
        self.caliberateSensor()

        self.running = True

        threading.Thread(target=self.updateData).start()
        time.sleep(0.5)
        threading.Thread(target=self.updateLine1).start()
        threading.Thread(target=self.updateLine2).start()
        threading.Thread(target=self.updateLine3).start()

    def getSerialData(self):
        line = self.mpu.readline().decode('utf-8')
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

    def getFilteredData(self,n):
        i=1
        sumax=0
        sumay=0
        sumaz=0
        sumgx=0
        sumgy=0
        sumgz=0
        while(i<=n):
            data=self.getSerialData()
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

    def caliberateSensor(self):
        print('Caliberating sensor, make sure your sensor is at rest...')
        data = self.getSerialData()
        self.offsetax=data[0]
        self.offsetay=data[1]
        self.offsetaz=data[2]
        self.offsetgx=data[3]
        self.offsetgy=data[4]
        self.offsetgz=data[5]

        # return [offsetax,offsetay,offsetaz,offsetgx,offsetgy,offsetgz]

    def updateData(self):
        while self.running:
            # self.data = self.getFilteredData(5)
            self.data.append(self.getFilteredData(5))
            # print(self.data)

    def getAccPitch(self):
        # print(self.data)
        if self.orient==3:
            if self.data[-1][2]==0:
                return math.pi/2
            return math.atan(self.data[-1][0]/self.data[-1][2]) 
        if self.orient==1:
            if self.data[-1][0]==0:
                print('Perp')
                return math.pi/2
            return math.atan(self.data[-1][2]/self.data[-1][0])

    def updateLine1(self):
        while self.running:
            a = self.getAccPitch()
            self.accAngle = a
            # self.canvas.delete("all")
            x2,y2 = self.giveP2(self.x11,self.y11,-a,self.len1)
            # canvas.create_oval()
            # self.canvas.create_line(self.x11,self.y11,x2,y2,fill=self.color1, width=self.width1)
            self.canvas.coords(self.line1,self.x11,self.y11,x2,y2)

    def updateLine2(self):
        z=0
        last_time = 0

        while self.running:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time

            z+=(self.data[-1][4]-self.offsetgy)*dt
            # print(f'Angle is {math.degrees(z)}')
            self.gyroAngle = z
            # print(f'gyro angle is {z}')
            x2,y2 = self.giveP2(self.x12,self.y12,-z,self.len2)
            # self.canvas.delete("all")
            # self.canvas.create_line(self.x12,self.y12,x2,y2,fill=self.color2, width=self.width2)
            self.canvas.coords(self.line2,self.x12,self.y12,x2,y2)

    def updateLine3(self):
        # print('here')
        while True:
            compAngle = self.alpha*self.gyroAngle+((1-self.alpha)*self.accAngle)
            x2,y2 = self.giveP2(self.x13,self.y13,-compAngle,self.len3)
            self.canvas.coords(self.line3,self.x13,self.y13,x2,y2)
            # print(f'Comp angle is {compAngle}')

    #a = angle from y axis(of tkinter) in anti clockwise direction, l is length of line.
    def giveP2(self,x1,y1,a,l):
        x2 = x1 + l*(math.sin(a))
        y2 = y1 + l*(math.cos(a))

        return x2,y2

    def stop_code(self):
        self.running=False
        time.sleep(1)
        exit()

    def buil_ui(self):
        self.root.title("Filters Visualization")
        self.canvas = tk.Canvas(self.root, width=700, height=400, bg="white")
        self.canvas.pack()

        self.line1 = self.canvas.create_line(0,0,0,0,fill=self.color1, width=self.width1)
        self.line2 = self.canvas.create_line(0,0,0,0,fill=self.color2, width=self.width2)
        self.line3 = self.canvas.create_line(0,0,0,0,fill=self.color3, width=self.width3)

        self.canvas.create_text(self.x11,self.y11-10,text="Using Accelerometer",font=('Segoe UI', 10),fill=self.color1)
        self.canvas.create_text(self.x12,self.y12-10,text="Using Gyroscope",font=('Segoe UI', 10),fill=self.color2)  
        self.canvas.create_text(self.x13,self.y13-10,text="Complementary filter",font=('Segoe UI', 10),fill=self.color3)  

        stop_btn = tk.Button(root,text="STOP",bg='red',command=self.stop_code)
        # stop_btn.pack()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
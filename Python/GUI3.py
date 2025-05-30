from tkinter import *
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import serial
import threading

class App():
    def __init__(self,root):
        self.root = root
        self.X = []
        self.Y = []
        self.X_display = []
        self.Y_display = []
        self.view_length = 100

        self.mpu = serial.Serial('COM3',115200)
        line1 = self.mpu.readline().decode('utf-8')

        self.build_ui()

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

    def build_ui(self):
        self.root.title('Drone EP1 Dashboard')
        self.root.geometry('900x500')
        self.root.configure(bg="#1e1e1e")

        mpu_heading = Label(self.root, text="MPU6050 Data",fg="white", bg="#1e1e1e", font=('Segoe UI', 20, 'bold'))
        mpu_heading.pack(anchor=CENTER)



        # self.fig,self.ax = plt.subplots(figsize=(2, 2))
        # self.ax.set(title="AccX",xlabel='Index',ylabel='m/s^2')
        # self.ax.set_ylim(0,16)
        # self.ax.plot(self.X_display,self.Y_display)

        self.fig = Figure(figsize=(2, 2), dpi=100)
        self.ax = self.fig.add_subplot(111)

        # self.ax.set_facecolor("#2b2b2b")
        # self.ax.tick_params(axis='x', colors='red', labelsize=6)
        # self.ax.tick_params(axis='y', colors='red', labelsize=6)
        self.ax.set_ylim(-20, 20)

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        # update graph after building ui
        update_arrays_thread = threading.Thread(target=self.updateArrays)
        update_arrays_thread.start()
        update_graph_thread = threading.Thread(target=self.updateGraphLoop)
        update_graph_thread.start()

    def updateArrays(self):
        i=1
        while True:
            data = self.getSerialData()
            if data==[]:
                pass
            else:
                self.X.append(i)
                self.Y.append(data[0])
                if(len(self.X)<=self.view_length):
                    self.X_display = self.X
                    self.Y_display = self.Y
                else:
                    self.X_display = self.X[-self.view_length+1:]
                    self.Y_display = self.Y[-self.view_length+1:]
            i+=1

    def updateGraphLoop(self):
        while True:
                self.ax.clear()
                self.ax.plot(self.X_display,self.Y_display)
                self.canvas.draw()


if __name__ == '__main__':
    root = Tk()
    app = App(root)
    root.mainloop()

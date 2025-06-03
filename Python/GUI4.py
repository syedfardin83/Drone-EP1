import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time
import serial 

class RealtimeGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drone EP1 Dashboard")
        self.root.configure(bg="#1e1e1e")

        self.graph_titles = ["AccX", "AccY", "AccZ", "GyroX", "GyroY", "GyroZ"]
        self.graph_colors = ["cyan", "magenta", "yellow", "lime", "orange", "red"]
        self.data = [[] for _ in range(6)]
        self.display_data = [[] for _ in range(6)]
        self.indices = []
        self.display_indices = []
        self.max_points = 500
        self.view_width = 100
        self.figures = []
        self.axes = []
        self.value_labels = []
        self.lines = []
        self.canvases = []

        self.linewidth=0.8

        self.running = True

        self.mpu = serial.Serial('COM3',115200)
        line1 = self.mpu.readline().decode('utf-8')

        self.build_ui()
    
    def stop(self):
        self.running=False
        exit()

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
        mpu_heading = tk.Label(root, text="MPU6050 Data",fg="white", bg="#1e1e1e", font=('Segoe UI', 20, 'bold'))
        mpu_heading.pack(anchor=tk.CENTER)
        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.pack(padx=10, pady=10)

        for i in range(6):
            graph_frame = tk.Frame(frame, bg="#1e1e1e")
            graph_frame.grid(row=i//3*3, column=i%3, padx=10, pady=10)

            title_label = tk.Label(graph_frame, text=self.graph_titles[i], fg="white", bg="#1e1e1e", font=('Segoe UI', 10))
            title_label.pack()

            fig = Figure(figsize=(2.5, 2), dpi=100, facecolor='#2b2b2b')
            ax = fig.add_subplot(111)
            ax.set_facecolor("#2b2b2b")
            ax.tick_params(axis='x', colors='white', labelsize=6)
            ax.tick_params(axis='y', colors='white', labelsize=6)
            ax.set_ylim(-20, 20)
            ax.set_xlim(0, self.view_width)
            ax.grid(True, color='gray', linestyle='--', linewidth=0.3)

            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas.get_tk_widget().configure(bg='#2b2b2b', highlightthickness=0)
            canvas.get_tk_widget().pack()
            canvas.draw()

            value_label = tk.Label(graph_frame, text="0.00", fg="white", bg="#1e1e1e", font=('Segoe UI', 9))
            value_label.pack()
            self.value_labels.append(value_label)

            self.figures.append(fig)
            self.axes.append(ax)
            self.canvases.append(canvas)
            # self.lines.append(line)
  
        stop_btn = tk.Button(self.root, text="STOP",command=self.stop)
        stop_btn.pack()

        update_arrays_thread = threading.Thread(target=self.updateArrays)
        update_arrays_thread.start()
        update_graphs_thread = threading.Thread(target=self.updateGraphsLoop)
        update_graphs_thread.start()

    def updateArrays(self):
        i=1
        while self.running:
            data = self.getSerialData()
            if data==[]:
                pass
            else:
                #Updating the main data arrays
                self.indices.append(i)
                for j in range(6):
                    self.data[j].append(data[j])

                # Updating the display arrays
                if(len(self.indices)<=self.view_width):
                    self.display_data = self.data
                    self.display_indices = self.indices
                else:
                    self.display_indices = self.indices[-self.view_width:]
                    self.display_data = [axis_data[-self.view_width:] for axis_data in self.data]
            i+=1

            print(f'X length = {len(self.indices)}')
            print(f'Y length = {len(self.data[1])}')
            # print(f'Y = {self.data[0]}')

    def updateGraphsLoop(self):
        while self.running:
            for j in range(6):
                self.axes[j].clear()
                self.axes[j].plot(self.display_indices,self.display_data[j],color=self.graph_colors[j],linewidth=self.linewidth)
                self.canvases[j].draw()

                self.value_labels[j].config(text=str(self.data[j][-1]))

if __name__ == "__main__":
    root = tk.Tk()
    app = RealtimeGraphApp(root)
    root.mainloop()

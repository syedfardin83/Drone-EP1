import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time
import random

# Dummy function to simulate sensor data — replace this with your actual getData()
def getData():
    return [random.uniform(-10, 10) for _ in range(6)]

class RealtimeGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MPU6050 Realtime Graphs")
        self.root.configure(bg="#1e1e1e")

        self.graph_titles = ["AccX", "AccY", "AccZ", "GyroX", "GyroY", "GyroZ"]
        self.graph_colors = ["cyan", "magenta", "yellow", "lime", "orange", "red"]
        self.graph_data = [[0]*100 for _ in range(6)]
        self.value_labels = []

        self.figures = []
        self.axes = []
        self.lines = []

        self.build_ui()
        self.running = True
        threading.Thread(target=self.update_loop, daemon=True).start()

    def build_ui(self):
        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.pack(padx=10, pady=10)

        for i in range(6):
            graph_frame = tk.Frame(frame, bg="#1e1e1e")
            graph_frame.grid(row=i//3*2, column=i%3, padx=10, pady=10)

            title_label = tk.Label(graph_frame, text=self.graph_titles[i], fg="white", bg="#1e1e1e", font=('Segoe UI', 10))
            title_label.pack()

            fig = Figure(figsize=(2.5, 2), dpi=100)
            ax = fig.add_subplot(111)
            ax.set_facecolor("#2b2b2b")
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            ax.set_ylim(-20, 20)
            ax.grid(True, color='gray', linestyle='--', linewidth=0.3)
            line, = ax.plot(self.graph_data[i], color=self.graph_colors[i], linewidth=1)

            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas.get_tk_widget().pack()
            canvas.draw()

            value_label = tk.Label(graph_frame, text="0.00", fg="white", bg="#1e1e1e", font=('Segoe UI', 9))
            value_label.pack()
            self.value_labels.append(value_label)

            self.figures.append(fig)
            self.axes.append(ax)
            self.lines.append(line)

    def update_loop(self):
        while self.running:
            data = getData()
            for i in range(6):
                self.graph_data[i].append(data[i])
                self.graph_data[i].pop(0)
                self.lines[i].set_ydata(self.graph_data[i])
                self.value_labels[i].config(text=f"{data[i]:.2f}")
                self.figures[i].canvas.draw()
            time.sleep(0.05)

if __name__ == "__main__":
    root = tk.Tk()
    app = RealtimeGraphApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import threading
import time

# Replace this with your actual MPU6050 reading function
def getData():
    import random
    return [random.uniform(-10, 10) for _ in range(6)]

class RealtimeGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MPU6050 Realtime Graphs")
        self.root.configure(bg="#1e1e1e")

        style = ttk.Style()
        style.theme_use('default')
        style.configure('.', background='#1e1e1e', foreground='white', font=('Segoe UI', 10))

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
            fig = Figure(figsize=(2.5, 2), dpi=100)
            ax = fig.add_subplot(111)
            ax.set_facecolor("#2b2b2b")
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            ax.set_title(self.graph_titles[i], color='white', fontsize=10)
            ax.set_ylim(-20, 20)
            line, = ax.plot(self.graph_data[i], color=self.graph_colors[i], linewidth=1.5)

            canvas = FigureCanvasTkAgg(fig, master=frame)
            plot_widget = canvas.get_tk_widget()
            plot_widget.grid(row=i//3*2, column=i%3, padx=10, pady=(0, 5))
            canvas.draw()

            value_label = tk.Label(frame, text="0.00", fg="white", bg="#1e1e1e", font=('Segoe UI', 10, 'bold'))
            value_label.grid(row=i//3*2+1, column=i%3)
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

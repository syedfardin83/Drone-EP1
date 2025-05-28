import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time

# Dummy function to simulate sensor data — replace this with your actual getData()
def getData():
    import random
    return [random.uniform(-10, 10) for _ in range(6)]

class RealtimeGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MPU6050 Realtime Graphs")
        self.root.configure(bg="#1e1e1e")

        self.graph_titles = ["AccX", "AccY", "AccZ", "GyroX", "GyroY", "GyroZ"]
        self.graph_colors = ["cyan", "magenta", "yellow", "lime", "orange", "red"]
        self.graph_data = [[] for _ in range(6)]
        self.max_points = 500
        self.view_width = 100
        self.scroll_indices = [0] * 6
        self.value_labels = []
        self.scrollbars = []
        self.figures = []
        self.axes = []
        self.lines = []

        self.auto_scroll = True

        self.build_ui()
        self.running = True
        threading.Thread(target=self.update_loop, daemon=True).start()

    def build_ui(self):
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
            line, = ax.plot([], color=self.graph_colors[i], linewidth=0.8)

            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas.get_tk_widget().configure(bg='#2b2b2b', highlightthickness=0)
            canvas.get_tk_widget().pack()
            canvas.draw()

            value_label = tk.Label(graph_frame, text="0.00", fg="white", bg="#1e1e1e", font=('Segoe UI', 9))
            value_label.pack()
            self.value_labels.append(value_label)

            scrollbar = tk.Scale(graph_frame, from_=0, to=0, orient="horizontal", length=200, bg="#1e1e1e",
                                 troughcolor="#333333", fg="white", highlightthickness=0, showvalue=0,
                                 sliderlength=10, width=6,
                                 command=lambda val, i=i: self.scroll_graph(i, int(val)))
            scrollbar.pack(pady=5)
            self.scrollbars.append(scrollbar)

            self.figures.append(fig)
            self.axes.append(ax)
            self.lines.append(line)

        btn = tk.Button(self.root, text="Recent", command=self.set_auto_scroll, bg="#333", fg="white", font=('Segoe UI', 9))
        btn.pack(pady=10)

    def set_auto_scroll(self):
        self.auto_scroll = True

    def scroll_graph(self, i, val):
        self.auto_scroll = False
        self.scroll_indices[i] = val
        self.update_graph(i)

    def update_graph(self, i):
        start = self.scroll_indices[i]
        end = start + self.view_width
        data_slice = self.graph_data[i][start:end]
        self.lines[i].set_data(range(len(data_slice)), data_slice)
        self.axes[i].set_xlim(0, self.view_width)
        self.axes[i].figure.canvas.draw()

    def update_loop(self):
        while self.running:
            data = getData()
            for i in range(6):
                self.graph_data[i].append(data[i])
                if len(self.graph_data[i]) > self.max_points:
                    self.graph_data[i].pop(0)

                self.value_labels[i].config(text=f"{data[i]:.2f}")
                self.scrollbars[i].config(to=max(0, len(self.graph_data[i]) - self.view_width))

                if self.auto_scroll:
                    self.scroll_indices[i] = max(0, len(self.graph_data[i]) - self.view_width)

                self.update_graph(i)
            time.sleep(0.05)

if __name__ == "__main__":
    root = tk.Tk()
    app = RealtimeGraphApp(root)
    root.mainloop()

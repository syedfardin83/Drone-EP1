import tkinter as tk
from tkinter import ttk
import serial
import time
import threading

# --- Serial Setup ---
arduino = serial.Serial('COM3', 9600)
time.sleep(2)

# --- Tkinter Setup ---
root = tk.Tk()
root.title("Arduino Control Panel")
root.geometry("420x300")
root.configure(bg="#1e1e1e")  # Dark background

val1 = tk.IntVar()
val2 = tk.IntVar()
response_var = tk.StringVar(value="No response yet")

# --- Dark Theme Styling ---
style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel", background="#1e1e1e", foreground="#ffffff", font=("Segoe UI", 11))
style.configure("TScale", background="#1e1e1e", troughcolor="#3a3a3a", sliderthickness=20)
style.map("TScale",
    background=[('active', '#4caf50')],
    troughcolor=[('active', '#4caf50')]
)
style.configure("TButton", background="#333333", foreground="#ffffff", font=("Segoe UI", 10, "bold"))

# --- Send to Arduino ---
def send_to_arduino():
    msg = f"{val1.get()} {val2.get()}\n"
    try:
        arduino.write(msg.encode())
    except Exception as e:
        response_var.set(f"Write Error: {e}")

def on_slider_release(event):
    send_to_arduino()

# --- Serial Read Thread ---
def read_from_arduino():
    while True:
        try:
            if arduino.in_waiting:
                line = arduino.readline().decode().strip()
                response_var.set("Arduino: " + line)
        except:
            pass

threading.Thread(target=read_from_arduino, daemon=True).start()

# --- UI Layout ---
ttk.Label(root, text="Slider 1").grid(row=0, column=0, padx=20, pady=10, sticky="w")
slider1 = ttk.Scale(root, from_=0, to=255, orient="horizontal", variable=val1)
slider1.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
slider1.bind("<ButtonRelease-1>", on_slider_release)

ttk.Label(root, text="Slider 2").grid(row=1, column=0, padx=20, pady=10, sticky="w")
slider2 = ttk.Scale(root, from_=0, to=255, orient="horizontal", variable=val2)
slider2.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
slider2.bind("<ButtonRelease-1>", on_slider_release)

ttk.Label(root, text="Response:").grid(row=2, column=0, padx=20, pady=20, sticky="w")
ttk.Label(root, textvariable=response_var, foreground="#4caf50", background="#1e1e1e").grid(row=2, column=1, padx=20, pady=20, sticky="w")

root.columnconfigure(1, weight=1)

# --- Exit Cleanly ---
def on_close():
    try:
        arduino.close()
    except:
        pass
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()

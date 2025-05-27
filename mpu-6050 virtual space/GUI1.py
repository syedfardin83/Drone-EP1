import tkinter as tk
import serial 
import threading

def exit_code():
    exit()

def readSerial():
    # print("here")

    mpu = serial.Serial('COM3',115200)

    while True:
        # print("here")
        line = mpu.readline().decode('utf-8')
        # print(type(line))

        a = line.strip().split(',')
        b=[]
        for i in a:
            try:
                b.append(float(i))
            except:
                pass
        print(b)
        try:
            entry_Accelx.delete(0,tk.END)
            entry_Accelx.insert(0,str(b[0]))

            entry_Accely.delete(0,tk.END)
            entry_Accely.insert(0,str(b[1]))

            entry_Accelz.delete(0,tk.END)
            entry_Accelz.insert(0,str(b[2]))

            entry_gx.delete(0,tk.END)
            entry_gx.insert(0,str(b[3]))

            entry_gy.delete(0,tk.END)
            entry_gy.insert(0,str(b[4]))

            entry_gz.delete(0,tk.END)
            entry_gz.insert(0,str(b[5]))
        except:
            pass



read_serial_thread = threading.Thread(target=readSerial)

read_serial_thread.start()

# Create the main window
root = tk.Tk()

# Set the title of the window
root.title("Sensor Data")

# Set window size
root.geometry("600x300")

# Set background color
root.configure(bg="#001f3d")  # Dark blue background

# Create the header for Accelerometer Data
heading_accel = tk.Label(root, text="Accelerometer Data", font=("Helvetica Neue", 18, "bold"), fg="white", bg="#001f3d")
heading_accel.pack(pady=10)

# Create a frame to hold the accelerometer entry boxes horizontally
frame_accel = tk.Frame(root, bg="#001f3d")
frame_accel.pack(pady=10)

# Accelerometer labels and entry boxes (arranged horizontally)
label_accel_Accelx = tk.Label(frame_accel, text="Accelx", font=("Helvetica Neue", 12), fg="white", bg="#001f3d")
label_accel_Accelx.grid(row=0, column=0, padx=10)

entry_Accelx = tk.Entry(frame_accel, font=("Helvetica Neue", 12), bd=2, width=10)  # Smaller width
entry_Accelx.grid(row=0, column=1, padx=10)
entry_Accelx.insert(0, "Accelx")

label_accel_Accely = tk.Label(frame_accel, text="Accely", font=("Helvetica Neue", 12), fg="white", bg="#001f3d")
label_accel_Accely.grid(row=0, column=2, padx=10)

entry_Accely = tk.Entry(frame_accel, font=("Helvetica Neue", 12), bd=2, width=10)  # Smaller width
entry_Accely.grid(row=0, column=3, padx=10)
entry_Accely.insert(0, "Accely")

label_accel_z = tk.Label(frame_accel, text="Accelz", font=("Helvetica Neue", 12), fg="white", bg="#001f3d")
label_accel_z.grid(row=0, column=4, padx=10)

entry_Accelz = tk.Entry(frame_accel, font=("Helvetica Neue", 12), bd=2, width=10)  # Smaller width
entry_Accelz.grid(row=0, column=5, padx=10)
entry_Accelz.insert(0, "xz")

# Create the header for Gyro Data
heading_gyro = tk.Label(root, text="Gyro Data", font=("Helvetica Neue", 18, "bold"), fg="white", bg="#001f3d")
heading_gyro.pack(pady=20)

# Create a frame to hold the Gyro entry boxes horizontally
frame_gyro = tk.Frame(root, bg="#001f3d")
frame_gyro.pack(pady=10)

# Gyro labels and entry boxes (arranged horizontally)
label_gyro_gx = tk.Label(frame_gyro, text="Gyro x", font=("Helvetica Neue", 12), fg="white", bg="#001f3d")
label_gyro_gx.grid(row=0, column=0, padx=10)

entry_gx = tk.Entry(frame_gyro, font=("Helvetica Neue", 12), bd=2, width=10)  # Smaller width
entry_gx.grid(row=0, column=1, padx=10)
entry_gx.insert(0, "Gyro x")

label_gyro_gy = tk.Label(frame_gyro, text="Gyro y", font=("Helvetica Neue", 12), fg="white", bg="#001f3d")
label_gyro_gy.grid(row=0, column=2, padx=10)

entry_gy = tk.Entry(frame_gyro, font=("Helvetica Neue", 12), bd=2, width=10)  # Smaller width
entry_gy.grid(row=0, column=3, padx=10)
entry_gy.insert(0, "Gyro y")

label_gyro_gz = tk.Label(frame_gyro, text="Gyro z", font=("Helvetica Neue", 12), fg="white", bg="#001f3d")
label_gyro_gz.grid(row=0, column=4, padx=10)

entry_gz = tk.Entry(frame_gyro, font=("Helvetica Neue", 12), bd=2, width=10)  # Smaller width
entry_gz.grid(row=0, column=5, padx=10)
entry_gz.insert(0, "Gyro z")

stop_btn = tk.Button(root,text="STOP",bg="red",command=exit_code)
stop_btn.pack(padx=15,pady=15)

# Run the Tkinter event loop
root.mainloop()

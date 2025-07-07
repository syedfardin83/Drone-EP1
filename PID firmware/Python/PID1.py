import serial
import time
import threading
import tkinter as tk

class App:
    def __init__(self,root):
        self.root = root
        self.running = True

        self.connect_serial()
        self.check_sensor()
        
        self.offsets = [0,0,0,0,0,0]

        #mpu6050 data
        self.filtered_data = []
        self.n_avg = 5

        self.build_ui()
        time.sleep(1)
        threading.Thread(target=self.updateFilteredData).start()
        time.sleep(0.5)
        self.calliberateSensor()
        threading.Thread(target=self.updateEntries).start()

    def connect_serial(self):
        #Connect to mpu serial
        try:
            self.mpu = serial.Serial('COM3',115200)
            _ = self.mpu.readline().decode('utf-8')
            print('#Serial successfully connected.')
        except Exception as e:
            print('#Serial connection error! Exitting...')
            time.sleep(1)
            exit()

    def check_sensor(self):
        print('#Checking for MPU6050 sensor...')
        sample_data = self.getSerialData()
        for i in range(6):
            if type(sample_data[i]) != float:
                print('#Invalid sensor data found! Exiting...')
                exit()
        print('#Sensor good to go!')

    def calliberateSensor(self):
        print('#Calliberating sensor...')
        for i in range(6):
            self.offsets[i] = self.filtered_data[-1][i]
        print(self.offsets)

    def stop(self):
        print('#Exiting program...')
        time.sleep(0.5)
        self.running = False
        time.sleep(1)
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

    def updateFilteredData(self):
        while self.running:
            data = [0,0,0,0,0,0]
            filtered_data = [0,0,0,0,0,0]
            for _ in range(self.n_avg):
                read_data = self.getSerialData()
                for i in range(6):
                    data[i] = data[i]+read_data[i]
            
            for i in range(6):
                filtered_data[i] = data[i]/self.n_avg
            self.filtered_data.append(filtered_data)

    def build_ui(self):
        self.motor_entries = []
        self.sensor_entries = []

        # Set a title for the window
        self.root.title("MPU6050 and Motor Monitor")

        # Create a grid layout
        motor_labels = ['M1', 'M2', 'M3', 'M4']
        sensor_labels = ['AccX', 'GyroX', 'AccY', 'GyroY', 'AccZ', 'GyroZ']

        # Motor entries (2x2 grid on the left)
        for i, label in enumerate(motor_labels):
            row = i // 2
            col = i % 2
            tk.Label(self.root, text=label).grid(row=row * 2, column=col, padx=10, pady=5)
            entry = tk.Entry(self.root, width=10)
            entry.grid(row=row * 2 + 1, column=col, padx=10, pady=5)
            self.motor_entries.append(entry)

        # Sensor entries (3x2 grid on the right)
        for i, label in enumerate(sensor_labels):
            row = i // 2
            col = 3 + (i % 2)  # Place in columns 3 and 4
            tk.Label(self.root, text=label).grid(row=row * 2, column=col, padx=10, pady=5)
            entry = tk.Entry(self.root, width=10)
            entry.grid(row=row * 2 + 1, column=col, padx=10, pady=5)
            self.sensor_entries.append(entry)

        # Stop button below
        stop_btn = tk.Button(self.root, text="EXIT", command=self.stop, fg="white", bg="red")
        stop_btn.grid(row=7, column=0, columnspan=5, pady=20)

    def updateEntries(self):
        while self.running:
            for i in range(6):
                self.sensor_entries[i].delete(0,tk.END)
                self.sensor_entries[i].insert(0,str(round(self.filtered_data[-1][i]-self.offsets[i],2)))

    

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
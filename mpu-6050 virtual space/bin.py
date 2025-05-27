# def appendFile(str):
#     f = open('ho.txt','x')
#     f.close()

#     new = init+'\n'+str

#     f=open('hlo.txt','w')
#     f.write(new)
#     f.close

# appendFile('Hey')
# appendFile('Hi')

# from datetime import datetime
# print(datetime.now())

# from datetime import datetime
# # f = open(f'./logs/{str(datetime.now()).replace('.','/').replace(':','/')}.txt','r')
# f=open('logs/abc.txt','r')
# f.close()

# f = open('kjkhkh.txt','x')
# f.close()

# a = [1,2,3]
# print(str(a))

# import pyautogui
# import tkinter as tk
# import threading

# def updateCoord():
#     while True:
#         # Get current mouse position
#         x, y = pyautogui.position()
#         # print(y)
#         # print(f"Mouse position: ({x}, {y})")
#         entry1.delete(0,tk.END)
#         entry1.insert(0,str(x))
#         entry2.delete(0,tk.END)
#         entry2.insert(0,str(y))

# # Create main window

# root = tk.Tk()
# root.title("Mouse coordinates")
# root.configure(bg='#001f3f')  # Dark blue background
# root.geometry("500x100")

# # Styling
# label_font = ("Arial", 12)
# label_fg = "white"
# entry_bg = "#003366"
# entry_fg = "white"

# # Create a frame for horizontal layout
# form_frame = tk.Frame(root, bg=root['bg'])
# form_frame.pack(pady=20)

# # Username label and entry
# label1 = tk.Label(form_frame, text="X:", font=label_font, fg=label_fg, bg=root['bg'])
# label1.pack(side=tk.LEFT, padx=5)
# entry1 = tk.Entry(form_frame, bg=entry_bg, fg=entry_fg)
# entry1.pack(side=tk.LEFT, padx=10)

# # Password label and entry
# label2 = tk.Label(form_frame, text="Y:", font=label_font, fg=label_fg, bg=root['bg'])
# label2.pack(side=tk.LEFT, padx=5)
# entry2 = tk.Entry(form_frame, bg=entry_bg, fg=entry_fg)
# entry2.pack(side=tk.LEFT, padx=10)

# update_thread = threading.Thread(target=updateCoord)
# update_thread.start()


# # Run the application
# root.mainloop()

# screen dimensions:
# 1919x1079

# import pyautogui

# # Move mouse to coordinates (500, 300)
# pyautogui.moveTo(0, 0)

#virtual space in z coord:

# import serial

# mpu = serial.Serial('COM3',115200)
# line = mpu.readline().decode('utf-8')
# # this function returns an array
# def getData():
#     line = mpu.readline().decode('utf-8')

#     a = line.strip().split(',')
#     b=[]
#     for i in a:
#         try:
#             b.append(float(i))
#         except Exception as e:
#             print(e)
#             pass
#     return b

# z=0
# vz=0
# az=0
# while True:
#     data = getData()
#     ax=data[0]
#     ay=data[1]
#     az=round(data[2],1)

#     vz=vz+az+0.3
#     z=z+vz

#     vz=round(vz,1)
#     # print(z)
#     print(vz)
#     # print(round(az+0.3,1))

# import pandas as pd
# s = pd.Series([1.4,54.34,34.5])
# print(type(s[0]))

import random
import math

def n_avg_filter(n,arr):
    new_arr = []

    n_sets = int(math.ceil(len(arr)/n))
    i=1
    while(i<=n_sets):
        ll = n*(i-1)

        if i!=n_sets:
            ul = ll+(n-1)
        else:
            ul = len(arr)-1

        sum=0
        j=ll
        while(j<=ul):
            sum=sum+arr[j]
            j=j+1
        
        avg = sum/(ul-ll+1)

        new_arr.append(round(avg,1))
        i=i+1
    
    return new_arr

arr = [random.randint(1,10) for _ in range(random.randint(50,100))]
# arr = [1,2,3,4,5,6]
print(arr)
filtered_arr = n_avg_filter(10,arr)
print(filtered_arr)
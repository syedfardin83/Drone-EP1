import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('C:/Users/Syed Shabbir/Desktop/Fardin/Coding/Drone-EP1/IRLZ44N Motor control/Data/arduino_led.csv')
# print(data["Arduino Value"])
fig,ax = plt.subplots()

ax.set(xlabel="Arduino Value",ylabel="Source Voltage",title="IRLZ44N with LED PWD")
ax.plot(data["Arduino Value"],data["Source Voltage"])
fig.savefig('C:/Users/Syed Shabbir/Desktop/Fardin/Coding/Drone-EP1/IRLZ44N Motor control/Plots/plot1.png')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

def n_filter(n,arr):
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



# Load CSV file
df = pd.read_csv("logs/log1.csv")  # Replace with your actual filename

# Extract AccelY column
accel_y = df["AccelY"].to_list()
filtered_accel_y = n_filter(13,accel_y)
filtered_accel_y = pd.Series(filtered_accel_y)


# Plot the data
plt.figure(figsize=(10, 5))
plt.plot(filtered_accel_y, label="13 Filtered Accel Y", color='blue', marker='o')
plt.title("AccelY Line Graph")
plt.xlabel("Sample Index")
plt.ylabel("Acceleration (Y-axis)")
plt.grid(True)
plt.legend()

# Save to PNG
plt.savefig("plots/filtered_3_accely_plot.png")

# Optional: show the plot
# plt.show()

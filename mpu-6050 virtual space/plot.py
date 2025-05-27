import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
df = pd.read_csv("logs/log1.csv")  # Replace with your actual filename

# Extract AccelY column
accel_y = df["AccelY"]

# Plot the data
plt.figure(figsize=(10, 5))
plt.plot(accel_y, label="AccelY", color='blue', marker='o')
plt.title("AccelY Line Graph")
plt.xlabel("Sample Index")
plt.ylabel("Acceleration (Y-axis)")
plt.grid(True)
plt.legend()

# Save to PNG
plt.savefig("plots/accely_plot.png")

# Optional: show the plot
# plt.show()

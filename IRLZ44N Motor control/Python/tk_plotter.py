import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. Dummy CSV Creation (for easy testing) ---
# This section creates a sample 'arduino_led.csv' file
# in a 'Data' subfolder relative to where this Python script is run.
# You can comment this out in your actual project if your CSV is already present.

def create_dummy_csv():
    dummy_data = {
        "Arduino Value": [10, 50, 100, 150, 200, 250],
        "Source Voltage": [3.1, 3.3, 3.5, 3.8, 4.0, 4.2],
        "Temperature": [25.0, 25.5, 26.0, 26.5, 27.0, 27.5],
        "Current (mA)": [50, 100, 150, 200, 250, 300]
    }
    dummy_df = pd.DataFrame(dummy_data)

    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder_path = os.path.join(current_script_dir, 'Data')
    os.makedirs(data_folder_path, exist_ok=True) # Create 'Data' folder if it doesn't exist
    
    csv_path = os.path.join(data_folder_path, 'arduino_led.csv')
    dummy_df.to_csv(csv_path, index=False)
    return csv_path

# Create the dummy CSV when the script starts
default_csv_path = create_dummy_csv()
# --- End Dummy CSV Creation ---


class CSVPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Data Plotter")
        self.root.geometry("600x450") # Set initial window size
        self.root.resizable(False, False) # Make window non-resizable

        # Set a consistent padding for widgets
        self.padding = {'padx': 10, 'pady': 5}
        self.entry_width = 50

        # --- CSV File Path ---
        tk.Label(root, text="CSV File Path:").grid(row=0, column=0, sticky="w", **self.padding)
        self.csv_path_entry = tk.Entry(root, width=self.entry_width)
        self.csv_path_entry.grid(row=0, column=1, **self.padding)
        tk.Button(root, text="Browse CSV", command=self.browse_csv).grid(row=0, column=2, **self.padding)
        # Pre-fill with dummy CSV path
        self.csv_path_entry.insert(0, default_csv_path)

        # --- X-axis Column Name ---
        tk.Label(root, text="X-axis Column Name:").grid(row=1, column=0, sticky="w", **self.padding)
        self.x_col_entry = tk.Entry(root, width=self.entry_width)
        self.x_col_entry.grid(row=1, column=1, **self.padding)
        # Pre-fill with common column name from dummy data
        self.x_col_entry.insert(0, "Arduino Value")

        # --- Y-axis Column Name ---
        tk.Label(root, text="Y-axis Column Name:").grid(row=2, column=0, sticky="w", **self.padding)
        self.y_col_entry = tk.Entry(root, width=self.entry_width)
        self.y_col_entry.grid(row=2, column=1, **self.padding)
        # Pre-fill with common column name from dummy data
        self.y_col_entry.insert(0, "Source Voltage")

        # --- Plot Title ---
        tk.Label(root, text="Plot Title:").grid(row=3, column=0, sticky="w", **self.padding)
        self.title_entry = tk.Entry(root, width=self.entry_width)
        self.title_entry.grid(row=3, column=1, **self.padding)
        # Pre-fill with a default title
        self.title_entry.insert(0, "My Data Plot")

        # --- Output PNG File Path ---
        tk.Label(root, text="Save Plot As:").grid(row=4, column=0, sticky="w", **self.padding)
        self.output_path_entry = tk.Entry(root, width=self.entry_width)
        self.output_path_entry.grid(row=4, column=1, **self.padding)
        tk.Button(root, text="Browse Save Location", command=self.browse_save_location).grid(row=4, column=2, **self.padding)
        # Pre-fill with a suggested save path
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        plots_folder_path = os.path.join(current_script_dir, 'Plots')
        os.makedirs(plots_folder_path, exist_ok=True) # Create 'Plots' folder if it doesn't exist
        self.output_path_entry.insert(0, os.path.join(plots_folder_path, 'my_plot.png'))


        # --- Generate Plot Button ---
        tk.Button(root, text="Generate and Save Plot", command=self.generate_plot).grid(row=5, column=0, columnspan=3, pady=20)

        # --- Status Label ---
        self.status_label = tk.Label(root, text="", fg="blue")
        self.status_label.grid(row=6, column=0, columnspan=3, **self.padding)

    def browse_csv(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.csv_path_entry.delete(0, tk.END)
            self.csv_path_entry.insert(0, file_path)
            self.update_status(f"CSV selected: {os.path.basename(file_path)}", "blue")

    def browse_save_location(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if file_path:
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, file_path)
            self.update_status(f"Save location selected: {os.path.basename(file_path)}", "blue")

    def update_status(self, message, color="black"):
        self.status_label.config(text=message, fg=color)
        self.root.update_idletasks() # Update GUI immediately

    def generate_plot(self):
        csv_file = self.csv_path_entry.get()
        x_col = self.x_col_entry.get()
        y_col = self.y_col_entry.get()
        plot_title = self.title_entry.get()
        output_file = self.output_path_entry.get()

        # Basic input validation
        if not csv_file or not x_col or not y_col or not plot_title or not output_file:
            self.update_status("Error: All fields must be filled.", "red")
            return

        try:
            # 1. Load the CSV data
            self.update_status(f"Loading data from {os.path.basename(csv_file)}...", "blue")
            df = pd.read_csv(csv_file)

            # 2. Check if columns exist
            if x_col not in df.columns:
                self.update_status(f"Error: X-axis column '{x_col}' not found in CSV.", "red")
                return
            if y_col not in df.columns:
                self.update_status(f"Error: Y-axis column '{y_col}' not found in CSV.", "red")
                return

            # 3. Extract data for plotting
            x_data = df[x_col]
            y_data = df[y_col]

            # 4. Create the plot
            self.update_status("Generating plot...", "blue")
            fig, ax = plt.subplots(figsize=(10, 6)) # Create a figure and an axes object

            ax.plot(x_data, y_data, marker='o', linestyle='-', color='skyblue', label=f'{y_col} vs. {x_col}')

            # 5. Set titles and labels dynamically
            ax.set(xlabel=x_col, ylabel=y_col, title=plot_title)

            # Add grid and legend (optional, but good practice)
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.legend()
            plt.tight_layout() # Adjust layout to prevent labels from overlapping

            # 6. Save the plot as PNG
            self.update_status(f"Saving plot to {os.path.basename(output_file)}...", "blue")
            fig.savefig(output_file, dpi=300) # dpi for higher quality image

            # 7. Display the plot (blocking call, will keep window open)
            self.update_status("Plot generated and saved. Displaying plot...", "green")
            plt.show()

            # After plt.show() closes, update status
            self.update_status(f"Plot saved successfully to {output_file}", "green")

        except FileNotFoundError:
            self.update_status(f"Error: CSV file not found at '{csv_file}'", "red")
        except pd.errors.EmptyDataError:
            self.update_status(f"Error: CSV file '{csv_file}' is empty.", "red")
        except Exception as e:
            self.update_status(f"An unexpected error occurred: {e}", "red")
        finally:
            # Ensure the plot figure is closed to free memory after plt.show()
            # This is important if you plan to generate multiple plots without restarting the app
            plt.close(fig)


# --- Run the Tkinter application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = CSVPlotterApp(root)
    root.mainloop()


import matplotlib.pyplot as plt
import numpy as np
import os

# File path to your ECG data text file
file_path = "./ECG_DATA_TXT.txt"

# Check if the file exists
if not os.path.exists(file_path):
    print(f"Error: The file {file_path} does not exist.")
    exit(1)

# Read the ECG data from the text file
ecg_data = []
with open(file_path, 'r') as file:
    for line in file:
        try:
            # Convert each line to a float and append to the list
            ecg_data.append(float(line.strip()))
        except ValueError:
            # If there's a line that can't be converted, print an error and skip it
            print(f"Warning: Skipping invalid line: {line.strip()}")

# Check if data was read successfully
if len(ecg_data) == 0:
    print("Error: No valid data found in the file.")
    exit(1)

# Generate an arbitrary x-axis based on the length of ecg_data
x_values = np.arange(len(ecg_data))

# Plot the ECG data
plt.plot(x_values, ecg_data, label='ECG Voltage')
plt.xlabel('Time (arbitrary units)')
plt.ylabel('Voltage')
plt.title('Main ECG Graph')
plt.legend()
plt.show()

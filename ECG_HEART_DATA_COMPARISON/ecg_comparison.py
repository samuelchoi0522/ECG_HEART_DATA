import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.signal import find_peaks
from scipy.interpolate import interp1d
import csv

#file paths
apple_watch_csv_path = "/Users/sam/Desktop/Research Project/ECG_HEART_DATA_COMPARISON/apple_health_export/electrocardiograms/ECG_RECORDING_1.csv"
main_ecg_file_path = "/Users/sam/Desktop/Research Project/ECG_HEART_DATA_VISUALIZER/ECG_HEART_DATA/ECG_DATA_TXT.txt"

#check if files exist
if not os.path.exists(apple_watch_csv_path):
    print(f"Error: The file {apple_watch_csv_path} does not exist.")
    exit(1)

if not os.path.exists(main_ecg_file_path):
    print(f"Error: The file {main_ecg_file_path} does not exist.")
    exit(1)


apple_watch_data = []
with open(apple_watch_csv_path, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if len(row) > 0 and row[0].strip():
            try:
                apple_watch_data.append(float(row[0]))
            except ValueError:
                print(f"Warning: Skipping invalid line: {row}")

#convert µV to mV
apple_watch_data_mV = [value / 1000 for value in apple_watch_data]

main_ecg_data = []
with open(main_ecg_file_path, 'r') as file:
    for line in file:
        try:
            main_ecg_data.append(float(line.strip()))
        except ValueError:
            print(f"Warning: Skipping invalid line: {line.strip()}")

if len(apple_watch_data_mV) == 0:
    print("Error: No valid Apple Watch ECG data found in the file.")
    exit(1)

if len(main_ecg_data) == 0:
    print("Error: No valid main ECG data found in the file.")
    exit(1)

#sampling rates
sampling_rate_main = 2000
sampling_rate_apple_watch = 512.7  #assuming 512.7 Hz for Apple Watch ECG data

#generate time axes for the ECG data
time_main = np.arange(len(main_ecg_data)) / sampling_rate_main
time_apple_watch = np.arange(len(apple_watch_data_mV)) / sampling_rate_apple_watch

#interpolation of the apple watch ECG data to match the main ECG data time axis
interp_func = interp1d(time_apple_watch, apple_watch_data_mV, kind='linear', fill_value="extrapolate")
time_interp = np.arange(0, max(time_main), 1/sampling_rate_main)
apple_watch_interp = interp_func(time_interp)

#aligning the peaks using find_peaks
peaks_main, _ = find_peaks(main_ecg_data, height=0.5)
peaks_apple, _ = find_peaks(apple_watch_interp, height=0.2)

#check if peaks were found and align them
if len(peaks_main) > 0 and len(peaks_apple) > 0:
    time_shift = time_interp[peaks_apple[0]] - time_main[peaks_main[0]]
    time_main_shifted = time_main + time_shift

    plt.figure(figsize=(10, 6))

    plt.plot(time_main_shifted, main_ecg_data, label='Main ECG (2000 Hz)', color='blue')
    plt.plot(time_interp, apple_watch_interp, label='Apple Watch ECG (512.7 Hz)', color='red', linestyle='--')

    plt.xlabel('Time (seconds)')
    plt.ylabel('Voltage (mV)')
    plt.title('ECG Data Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()

else:
    print("No peaks were detected in one of the datasets.")

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks, savgol_filter
from matplotlib.animation import FuncAnimation
import time
import psutil
import csv

def moving_average(data, window_size):
    cumsum = np.cumsum(data)
    cumsum[window_size:] = cumsum[window_size:] - cumsum[:-window_size]
    return cumsum[window_size - 1:] / window_size

def normalize_data(data):
    min_val = np.min(data)
    max_val = np.max(data)
    if max_val == min_val:
        return data
    normalized_data = (data - min_val) / (max_val - min_val)
    return normalized_data

def baseline_correction(signal, window_size):
    if len(signal) < window_size:
        raise ValueError("Signal length should be greater than or equal to window_size.")
    baseline = np.convolve(signal, np.ones(window_size) / window_size, mode='same')
    corrected_signal = signal - baseline
    return corrected_signal

def detect_peaks(signal, threshold=0.8):
    peaks, _ = find_peaks(signal, height=threshold)
    return peaks

def low_pass_filter(signal, window_size):
    return moving_average(signal, window_size)

def savitzky_golay_filter(signal, window_size, order):
    if window_size % 2 == 0:
        window_size += 1  # Ensure window_length is odd
    return savgol_filter(signal, window_size, order)

start_time = time.time()
end_time = 0

def get_memory_usage():
    process = psutil.Process()
    mem = process.memory_info().rss / (1024 ** 2)  # in MB
    return f"Memory Usage: {mem:.2f} MB"

def analyze(chunk, peaks):
    global START
    global END
    global writer
        
    for i in range(0,len(chunk)):
        if(len(peaks)==0):
            END = round(END + 1.0, 5)
            break
        for peak in peaks:

            if(i == peak):
                END = round(END + i/len(chunk),5)
                writer.writerow([
                    round(START, 5),
                    round(END, 5),
                    "Water"
                ])
                
                writer.writerow([
                    round(END, 5),
                    round(END, 5),
                    "tissue"
                ])
                START = END
                break



def update_plot(frame):
    try:
        adc2.clear()
        row = next(csv_stream)
        adc2.extend(row['adc2'])

        adc2_filtered = savitzky_golay_filter(adc2, window_size, order=3)

        adc2_filtered = baseline_correction(adc2_filtered, window_size)
        #adc2_filtered = adc2_filtered[2500:-2500]
        peaks = detect_peaks(adc2_filtered, threshold=75)

        with open('result.csv', 'a', newline='') as file:
            global writer
            writer = csv.writer(file)
            analyze(adc2_filtered, peaks)
            
        ax.clear()

        ax.plot(adc2_filtered, label='Channel 2 filtered', color='r')
        ax.plot(peaks, [adc2_filtered[i] for i in peaks], 'bo', label='True Peaks')

        ax.annotate(get_memory_usage(), (0.75, 0.1), xycoords='axes fraction')

        end_time = time.time()
        elapsed_time = end_time - start_time
        ax.annotate(f"Time: {elapsed_time:.2f} s", (0.75, 0.05), xycoords='axes fraction')
        ax.set_xlim(0, CHUNK_SIZE)
        ax.set_ylim(-500, 1200)
        ax.set_xlabel('Index')
        ax.set_ylabel('Value')
        ax.legend()

        memory_usage_data.append(get_memory_usage())

    except StopIteration:
        ani3.event_source.stop()
        end_time = time.strftime("%Y-%m-d %H:%M:%S", time.localtime())
        print(f"End Time: {end_time}")

fig3, ax = plt.subplots()
with open('result.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["startTime","endTime","label"])
adc2 = []
window_size = 700
CHUNK_SIZE = 50000
START = round(0.0, 5)
END = round(0.0, 5)
file_path = 'Benchmark signal.csv'
csv_stream = pd.read_csv(file_path, chunksize=CHUNK_SIZE)

ani3 = FuncAnimation(fig3, update_plot, blit=False, interval=500,cache_frame_data=False)
memory_usage_data = []

plt.show()
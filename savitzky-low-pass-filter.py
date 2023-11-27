import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks, savgol_filter
from matplotlib.animation import FuncAnimation
import time
import psutil

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

# Initialize time variables
start_time = time.time()
end_time = 0

# Create a function to calculate memory usage
def get_memory_usage():
    process = psutil.Process()
    mem = process.memory_info().rss / (1024 ** 2)  # in MB
    return f"Memory Usage: {mem:.2f} MB"

def update_plot(frame):
    try:
        adc2.clear()
        row = next(csv_stream)
        adc2.extend(row['adc2'])

        # Apply low-pass filtering
        # adc2_low_pass = low_pass_filter(adc2, window_size)
        # adc2_low_pass = normalize_data(adc2_low_pass)

        # Apply Savitzky-Golay filtering (replacing median filter)
        adc2_low_pass = savitzky_golay_filter(adc2, window_size, order=3)

        adc2_low_pass = baseline_correction(adc2_low_pass, 5000)
        adc2_low_pass = adc2_low_pass[5000:-5000]
        peaks = detect_peaks(adc2_low_pass, threshold=75)

        ax3.clear()

        ax3.plot(adc2_low_pass, label='Channel 2 filtered', color='r')
        ax3.plot(peaks, [adc2_low_pass[i] for i in peaks], 'bo', label='True Peaks')

        ax3.annotate(get_memory_usage(), (0.75, 0.1), xycoords='axes fraction')

        end_time = time.time()
        elapsed_time = end_time - start_time
        ax3.annotate(f"Time: {elapsed_time:.2f} s", (0.75, 0.05), xycoords='axes fraction')

        ax3.set_xlabel('Index')
        ax3.set_ylabel('Value')
        ax3.legend()

        memory_usage_data.append(get_memory_usage())

    except StopIteration:
        ani3.event_source.stop()
        end_time = time.strftime("%Y-%m-d %H:%M:%S", time.localtime())
        print(f"End Time: {end_time}")

fig3, ax3 = plt.subplots()

adc2 = []
window_size = 700

file_path = 'Benchmark signal.csv'
csv_stream = pd.read_csv(file_path, chunksize=3000000)

ani3 = FuncAnimation(fig3, update_plot, blit=False, interval=1000, cache_frame_data=False)
memory_usage_data = []

plt.show()

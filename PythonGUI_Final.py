import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pywt
import random
import math

stop_animation = False
FPS=1
FREQ = 50000
TF = 2
CHUNK=math.floor(FREQ/FPS)
INTERVAL=math.floor(1000/FPS)
INTERVALFRAME = math.floor(FREQ/INTERVAL)
MIN_VALUE=0
MAX_VALUE=1000
adc2 = []

class Timer:
        def __init__(self) -> None:
            self.time=0.0
        def getTime(self):
             return round(self.time,2)
        def setTime(self, newTime):
             self.time=self.time+newTime

TIMER = Timer()

def wavelet_denoise(signal, wavelet='db4', level=5):
    """
    Apply wavelet denoising to a signal.

    Args:
        signal (numpy array): The input signal.
        wavelet (str): The wavelet function to use (default is 'db4').
        level (int): The level of decomposition (increase for more aggressive denoising).

    Returns:
        numpy array: The denoised signal.
    """
    # Decompose the signal into wavelet coefficients
    coeffs = pywt.wavedec(signal, wavelet, level=level)

    # Set threshold for coefficients
    threshold = np.median(np.abs(coeffs[-level])) / 0.6745

    # Apply soft thresholding to the coefficients
    denoised_coeffs = [pywt.threshold(c, threshold, mode='soft') for c in coeffs]

    # Reconstruct the denoised signal from the coefficients
    denoised_signal = pywt.waverec(denoised_coeffs, wavelet)

    return denoised_signal


def update_plot(frame):

    if stop_animation:
        return
    
    try:
        TIMER.setTime(CHUNK/FREQ)

        row = next(csv_stream)
        chunkToAdd=row['adc2']


        
        adc2.extend(wavelet_denoise(row['adc2']))

        if(len(adc2)>TF*FREQ):
            copy=adc2.copy()[CHUNK:]
            adc2.clear()
            adc2.extend(copy)




        ax1.clear()
        ax1.set_ylabel('Value')
        ax1.plot(adc2, label='Time passed: '+TIMER.getTime().__str__())
        ax1.set_xticks([])
        ax1.set_ylim(bottom=0, top=1000)
        ax1.legend()
    except StopIteration:
        ani1.event_source.stop()

def start_animation_func():
    global stop_animation
    if stop_animation==False:
        return
    stop_animation = False
    ani.event_source.start()

def stop_animation_func():
    global stop_animation
    stop_animation = True



    

# Create a Tkinter window
root = tk.Tk()
root.title("Tkinter GUI with Plot")

# Create a frame for the plot
plot_frame = ttk.Frame(root)
plot_frame.grid(row=1, column=1, padx=10, pady=10)


# Create left and right frames for radio buttons
left_frame = ttk.Frame(root)
left_frame.grid(row=1, column=0, padx=10, pady=10)
right_frame = ttk.Frame(root)
right_frame.grid(row=1, column=2, padx=10, pady=10)
top_frame=ttk.Frame(root)
top_frame.grid(row=0, column=1, padx=10, pady=10)

# Create start and stop buttons

StartButton = ttk.Button(top_frame, text="Start", command=start_animation_func)
EndButton = ttk.Button(top_frame, text="Stop", command=stop_animation_func)
StartButton.pack()
EndButton.pack()

# Create radio buttons on the left
normFunc_radioVar = tk.StringVar()
normButton1 = ttk.Radiobutton(left_frame, text = "NormaliseFunction 1", variable = normFunc_radioVar, value="Norm 1")
normButton2 = ttk.Radiobutton(left_frame, text = "NormaliseFunction 2", variable = normFunc_radioVar,value="Norm 2")
normButton1.pack()
normButton2.pack()

# Create radio buttons on the right
peakVar = tk.StringVar()
PeakDetector1 = ttk.Radiobutton(right_frame, text="Peak detector function 1",variable = peakVar, value="Func 1")
PeakDetector2 = ttk.Radiobutton(right_frame, text="Peak detector function 2",variable = peakVar,value="Func 2")
PeakDetector1.pack()
PeakDetector2.pack()

# Create an animation

fig1, ax1 = plt.subplots()
window_size = 700

file_path = 'IDP_signal_example.csv'
csv_stream = pd.read_csv(file_path, chunksize=CHUNK)

ani = FuncAnimation(fig1, update_plot, blit=False, interval=INTERVAL, frames=100)

plt.show()

#ani = FuncAnimation(fig, update_plot, frames=100, repeat=False, blit=False, interval=100)





root.mainloop()
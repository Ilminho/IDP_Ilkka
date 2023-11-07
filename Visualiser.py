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
from Timer import Timer
from queue import Queue
from threading import Thread
from time import time
from scipy.signal import find_peaks, savgol_filter
from Util import roundList, averageOfList


def Mazrah(signal, threshold=0.8):
    peaks, _ = find_peaks(signal, height=threshold)
    return peaks

def baseline_correction(signal, window_size):
    if len(signal) < window_size:
        raise ValueError("Signal length should be greater than or equal to window_size.")
    baseline = np.convolve(signal, np.ones(window_size) / window_size, mode='same')
    corrected_signal = signal - baseline
    return corrected_signal

def low_pass_filter(signal, window_size):
    return moving_average(signal, window_size)

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

def savitzky_golay_filter(signal, window_size, order):
    if window_size % 2 == 0:
        window_size += 1  # Ensure window_length is odd
    return savgol_filter(signal, window_size, order)



class PeakDetector():
    Mazrah=0


def Visualiser(file_path,FPS=16, FREQ=50000, TF=2 , normalize=True, peakDetector=PeakDetector.Mazrah, lowpass=True):

    stop_animation = False
    CHUNK=math.floor(FREQ/FPS)
    INTERVAL=math.floor(1000/FPS)
    INTERVALFRAME = math.floor(FREQ/INTERVAL)
    MIN_VALUE=0
    MAX_VALUE=3000
    adc2 = []
    listOfPeakDetectors=[Mazrah]

    TIMER = Timer()

    def detectPeaks(chunk,function=PeakDetector.Mazrah):
        return listOfPeakDetectors[function(chunk)]

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

        try:
            TIMER.addTime(CHUNK/FREQ)

            row = next(csv_stream)
            chunkToAdd=row['adc2']
            
            roundedChunk=roundList(chunkToAdd)

            ######
            
            ######
            
            
            #adc2Filtered = savgol_filter(chunkToAdd, 500, 2)

            print(roundedChunk)

            adc2.extend(wavelet_denoise(roundedChunk))
            
            
            

            if(len(adc2)>TF*FREQ):
                copy=adc2.copy()[CHUNK:]
                adc2.clear()
                adc2.extend(copy)
                
            

            arrayToPlot=np.array(adc2)
            
            peaks, _ = find_peaks(arrayToPlot, threshold=0.3, width=500)
            
            ax1.clear()
            ax1.set_ylabel('Value')
            ax1.plot(adc2, label='Time passed: '+TIMER.getTime().__str__())
            ax1.plot(peaks,[arrayToPlot[i] for i in peaks], 'bo', label='True Peaks (Low-Pass)')
            ax1.set_xticks([])
            ax1.set_ylim(bottom=MIN_VALUE, top=MAX_VALUE)
            ax1.legend()
        except StopIteration:
            ani.event_source.stop()



    fig1, ax1 = plt.subplots()
    window_size = 700
    csv_stream = pd.read_csv(file_path, chunksize=CHUNK)

    ani = FuncAnimation(fig1, update_plot, blit=False, interval=INTERVAL, cache_frame_data=False)
    plt.show()
            


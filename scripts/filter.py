import magic
import sys
import numpy as np
import matplotlib.pyplot as plt
import biosignalsnotebooks as bsnb
import pandas as pd
import h5py
from scipy.signal import filtfilt, butter, iirnotch, welch
import math


#For clear calculations with defined variables
#Input: Raw 10-bit ADC values
#Output: [-1.64, 1.64] mV
def transfer_function(signal):
  return (((np.array(signal) / 2**10) - 0.5) * 3300) / 1009
    

fpath_h5 = 'yn_test_christian_3_9_22_M.h5'
fs = 1000

data, header = bsnb.load(fpath_h5, get_header=True)
print("Data Sample:" + str(fpath_h5))

ch = "CH1" # Channel
sr = header["sampling rate"] 
resolution = 10 # Resolution (number of available bits)

signal_raw = np.array(data[ch])
signal_raw = transfer_function(signal_raw)
time = bsnb.generate_time(signal_raw, sr)

signal_meancorrect = signal_raw - np.mean(signal_raw)

#60Hz Notch Filter for Power Line Noise
b, a = iirnotch(60, 30, 1000)
signal_notched = filtfilt(b, a, signal_meancorrect)

# [Band Pass to demonstrate most prominent frequency range]
low_cutoff = 20
high_cutoff = 450

# Fourth Order Butterworth 
b, a = butter(10, [low_cutoff, high_cutoff], fs=1000, btype='bandpass')
signal_filtered = filtfilt(b, a, signal_notched)

#Rectify signal
signal_rect = abs(signal_filtered)

plt.figure()
plt.title("Raw signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (mV)")
plt.plot(time, signal_raw)

f, Pxx_den = welch(signal_raw, fs)
plt.figure()
plt.title("Raw signal PSD")
plt.semilogy(f, Pxx_den)
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD [V**2/Hz]')

plt.figure()
plt.title("Filtered signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (mV)")
plt.plot(time, signal_filtered)

f, Pxx_den = welch(signal_filtered, fs)
plt.figure()
plt.title("Filtered signal PSD")
plt.semilogy(f, Pxx_den)
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD [V**2/Hz]')

plt.show()
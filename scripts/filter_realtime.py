import time
import numpy as np
from scipy.signal import filtfilt, butter, iirnotch

def transfer_function1(signal):
  return (((np.array(signal) / 2**10) - 0.5) * 3300) / 1009

def transfer_function2(signal):
  return (((np.array(signal) / 2**6) - 0.5) * 3300) / 1009

#60Hz Notch Filter for Power Line Noise
b_notch, a_notch = iirnotch(60, 30, 1000)
# [Band Pass to demonstrate most prominent frequency range]
low_cutoff = 20
high_cutoff = 450
# Fourth Order Butterworth 
b, a = butter(10, [low_cutoff, high_cutoff], fs=1000, btype='bandpass')

packet_samples = np.load('sample_buffer.npy')
print(packet_samples)

while True:
    start=time.time()
    timmestamp = packet_samples[0]
    raw_data = packet_samples[1:]
    raw_data = transfer_function1(raw_data[:,0:4])
    raw_data = transfer_function2(raw_data[:,4:])
    notched_data = filtfilt(b_notch, a_notch, raw_data, axis=0)
    filtered_data = filtfilt(b, a, notched_data, axis=0)
    
    print(filtered_data)
    print(time.time()-start)
    # Function to send filtered_data here
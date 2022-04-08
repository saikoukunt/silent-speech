import time
import numpy as np
from scipy.signal import filtfilt, butter, iirnotch
import Packet

from bitalino import BITalino

def transfer_function1(signal):
  return (((np.array(signal) / 2**10) - 0.5) * 3300) / 1009

def transfer_function2(signal):
  return (((np.array(signal) / 2**6) - 0.5) * 3300) / 1009

#60Hz Notch Filter for Power Line Noise
b, a = iirnotch(60, 30, 1000)
# [Band Pass to demonstrate most prominent frequency range]
low_cutoff = 20
high_cutoff = 450
# Fourth Order Butterworth 
b, a = butter(10, [low_cutoff, high_cutoff], fs=1000, btype='bandpass')

# The macAddress variable on Windows can be "XX:XX:XX:XX:XX:XX" or "COMX"
# while on Mac OS can be "/dev/tty.BITalino-XX-XX-DevB" for devices ending with the last 4 digits of the MAC address or "/dev/tty.BITalino-DevB" for the remaining
macAddress = "20:19:07:00:80:4C"

# This example will collect data for 5 sec.

batteryThreshold = 30
acqChannels = [0, 1, 2, 3, 4, 5]
samplingRate = 1000
nSamples = 240

# Connect to BITalino
device = BITalino(macAddress)

# Set battery threshold
device.battery(batteryThreshold)

# Read BITalino version
print(device.version())

# Start Acquisition
device.start(samplingRate, acqChannels)

while True:
    timestamp = time.time()
    # Read samples
    raw_data = device.read(nSamples)
    raw_data = transfer_function1(raw_data[:,0:4])
    raw_data = transfer_function2(raw_data[:,4:])
    notched_data = filtfilt(b, a, raw_data)
    filtered_data = filtfilt(b, a, notched_data)
    packet = Packet.packet(timestamp, filtered_data)
    # Function to send packet here
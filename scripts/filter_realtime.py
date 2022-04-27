import time
import numpy as np
from scipy.signal import filtfilt, butter, iirnotch

class Filter():
	def __init__(self):
		#60Hz Notch Filter for Power Line Noise
		self.b_notch, self.a_notch = iirnotch(60, 30, 1000)
		# [Band Pass to demonstrate most prominent frequency range]
		low_cutoff = 20
		high_cutoff = 450
		# Fourth Order Butterworth 
		self.b, self.a = butter(10, [low_cutoff, high_cutoff], fs=1000, btype='bandpass')
    
	def transfer_function1(self, signal):
		return (((np.array(signal) / 2**10) - 0.5) * 3300) / 1009

	def transfer_function2(self, signal):
		return (((np.array(signal) / 2**6) - 0.5) * 3300) / 1009

	def run(self, input, output):
		while True:
			if (not input.empty()):
				raw_data = input.get()
				raw_data = np.array(raw_data).astype('float64')

				#print("\nTESTfilt: ", raw_data[:,1:5])
				#with open("testunfilt.txt", "a") as f:
				#	np.savetxt(f, raw_data)
					#f.write(str(raw_data))
				#	f.write("\n")
				
				raw_data[:,1:5] = self.transfer_function1(raw_data[:,1:5])
				raw_data[:,5:] = self.transfer_function2(raw_data[:,5:])
				raw_data[:,1:] = filtfilt(self.b_notch, self.a_notch, raw_data[:,1:], axis = 0)
				raw_data[:,1:] = filtfilt(self.b, self.a, raw_data[:,1:], axis = 0)

				
				#with open("testfilt.txt", "a") as f:
				#	np.savetxt(f, raw_data)
					#f.write(str(raw_data))
				#	f.write("\n")

				output.put(raw_data)

import csv
from bitalino import BITalino

import numpy as np

class EMGStream:
    def __init__(self):
        self.sample_buffer = np.zeros(shape=(240, 7))
        self.macAddress = "20:19:07:00:80:4C"
		self.batteryThreshold = 30
		self.acqChannels = [0, 1, 2, 3, 4, 5]
		self.samplingRate = 1000
		self.nSamples = 240
        self.device = BITalino(macAddress)
        print(self.device.version())        

    def get_buffer(self, output):
        
        self.device.battery(self.batteryThreshold)
        self.device.start(self.samplingRate, self.acqChannels)
        row = 0

        while True:
            

            sample = (self.device.read(self.nSamples)
           	sample = np.delete(sample, [0,4], 1)
            self.sample_buffer[row, :] = np.array(sample)
            #np.insert(sample_buffer, row, np.array(sample), 0)
            # print(sample)
            output.put(self.sample_buffer)
            np.save("sample_buffer", sample_buffer)

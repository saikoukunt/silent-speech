import csv
from bitalino import BITalino

import numpy as np

class EMGStream:
    def __init__(self):
        self.sample_buffer = np.zeros(shape=(240, 6))
        self.macAddress = "20:19:07:00:80:4C" 
		self.batteryThreshold = 30
		
        self.device = BITalino(self.macAddress)
        print(self.device.version())        

    def get_buffer(self, output):
        
        bufferSize = 240
        channels = [0, 1, 2, 3, 4, 5] #[10, 10, 10, 10, 6, 6] bit
        samplingRate = 1000 #Hz
        self.device.battery(self.batteryThreshold)
        self.device.start(samplingRate, channels)
        
        while True:       

            sample = (self.device.read(bufferSize)
           	sample = np.delete(sample, [0,4], 1)
            self.sample_buffer[0, :] = np.array(sample)
            output.put(self.sample_buffer)
            np.save("sample_buffer", sample_buffer)

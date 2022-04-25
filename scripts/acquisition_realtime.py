import csv
from bitalino import BITalino

import numpy as np

class EMGStream:
    def __init__(self):
        self.sample_buffer = np.zeros(shape=(240, 7))
        self.macAddress = "20:19:07:00:80:D4" 
        self.batteryThreshold = 30
        self.device = BITalino(self.macAddress)


    def get_buffer(self, output):

        print(self.device.version())  
        bufferSize = 240
        channels = [0, 1, 2, 3, 4, 5] #[10, 10, 10, 10, 6, 6] bit
        samplingRate = 1000 #Hz
        self.device.battery(self.batteryThreshold)

        self.device.start(samplingRate, channels)

        while True:
            #print("RUNNING..")
            sample = self.device.read(bufferSize)
            sample = np.delete(sample, [1,2,3,4], 1)
            #print(sample)
            self.sample_buffer = np.array(sample)
            #print(self.sample_buffer)
            output.put(self.sample_buffer)
            #np.save("sample_buffer", self.sample_buffer)

import csv
from bitalino import BITalino

import numpy as np

macAddress = "20:19:07:00:80:4C"
batteryThreshold = 30
acqChannels = [0, 1, 2, 3, 4, 5]
samplingRate = 1000
nSamples = 10

class EMGStream:
    def __init__(self):
        self.sample_buffer = np.zeros(shape=(240, 7))
        self.device = BITalino(macAddress)
        self.device.battery(batteryThreshold)
        print(self.device.version())        

    def get_buffer(self, output):
        
        self.device.start(samplingRate, acqChannels)
        row = 0

        while True:
            # get a new sample (you can also omit the timestamp part if you're not
            # interested in it)
            sample = (device.read(nSamples)
            sample.pop(0)
            self.sample_buffer[row, :] = np.array(sample)
            #np.insert(sample_buffer, row, np.array(sample), 0)
            # print(sample)
            row = row + 1
            if(row == 240):
                row = 0
                output.put(self.sample_buffer)
                #np.save("sample_buffer", sample_buffer)

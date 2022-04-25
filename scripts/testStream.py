import extract_data
import csv
import numpy as np

class EMGStream:
    def __init__(self):
        self.sample_buffer = np.zeros(shape=(240, 7))
        self.data, _,_,_ = extract_data.extract_data("../raw/Mouthed_14word_6_set10.txt","../raw/Mouthed_14word_6_set10_times.txt")

    def get_buffer(self, output): 

        for i in range(self.data.shape[0]):
            self.sample_buffer[i%240,:] = self.data[i,:] 
            if(i%240==239):
                output.put(self.sample_buffer)


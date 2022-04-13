from pylsl import StreamInlet, resolve_stream
import csv
import numpy as np


class EMGStream:
    def __init__(self,output):
        self.sample_buffer = np.zeros(shape=(240, 7))
        self.output = output

    def get_buffer(self):
        streams = resolve_stream('name', 'OpenSignals')
        inlet = StreamInlet(streams[0])
        row = 0

        while True:
            # get a new sample (you can also omit the timestamp part if you're not
            # interested in it)
            sample, timestamp = inlet.pull_sample()
            sample.pop(0)
            sample.insert(0, timestamp)
            self.sample_buffer[row, :] = np.array(sample)
            #np.insert(sample_buffer, row, np.array(sample), 0)
            # print(sample)
            row = row + 1
            if(row == 240):
                row = 0
                print(self.sample_buffer)
                #np.save("sample_buffer", sample_buffer)

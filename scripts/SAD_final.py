import numpy as np
from collections import deque
import pickle 
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd

class SAD():
    def __init__(self):
        self.globalIsFinished = False

        self.active_count = 0
        self.inactive_count = 0
        self.active_thresh = 3 
        self.inactive_thresh = 7
        self.isSpeech = False

        self.packet_length = 240
        self.window_length = 40
        self.skip = 20

        self.rms_window = deque([0,0,0,0,0])
        self.smooth_window = deque([0]*self.window_length)

        self.clf = pickle.load(open("classifier.pkl", 'rb'))
        self.scaler = pickle.load(open("scaler.pkl", 'rb'))
        
        self.data = None
        self.prev_data = deque()
        self.add_rows(self.prev_data, np.zeros((6,self.packet_length)), self.packet_length)
        self.speech_data = deque([])

    def rms(self, raw):
        rms_data = np.zeros(len(raw))
        for i in range(len(raw)):
            self.rms_window.popleft()
            self.rms_window.append(raw[i])
            rms_data[i] = np.sqrt(sum(np.square(self.rms_window)/5))

        return rms_data

    def smooth(self, rms_data):
        start = 0; end = self.skip; i = 0
        downsampled = np.zeros(int(len(rms_data)/self.skip))

        while start < len(rms_data):
            for i in range(self.skip):
                self.smooth_window.popleft()

            self.smooth_window.extend((rms_data[start:end]).tolist())
            downsampled[i] = np.mean(self.smooth_window, dtype=np.float64)
            start += self.skip; end += self.skip; i += 1

        return downsampled

    def pop_prev(self, n):
        for i in range(n):
            self.prev_data.popleft()

    def add_rows(self, deq, data, n):
        for i in range(n):
            deq.append((data[:,i]).tolist())

    def run(self, input, output):
        while True:
            if (not input.empty()):
                
                self.data = abs(np.transpose(input.get()))
            
                smoothed =  np.zeros((6,12))
                for i in range(6):
                    smoothed[i,:] = self.smooth(self.rms(self.data[i,:]))

                X = pd.DataFrame({
                    "Chan1": smoothed[0],
                    "Chan2": smoothed[1],
                    "Chan6": smoothed[5] 
                })
                X = self.scaler.transform(X)
                predicted = self.clf.predict(X)

                for i in range(len(smoothed)):
                    curr_data = self.data[:,i*self.skip:(i+1)*self.skip]
                    if self.isSpeech:
                        # update inactive counter
                        if predicted[i]:
                            self.inactive_count = 0
                        else:
                            self.inactive_count += 1
                            self.active_count = 0

                        # check if is speech
                        if self.inactive_count > self.inactive_thresh:
                            self.isSpeech = False
                            # speech event is over, send the speech data
                            output.put(np.array(self.speech_data))
                            self.speech_data = deque([])
                        else:
                            self.add_rows(self.speech_data, curr_data, 20)

                    else:
                        # update active counter
                        if predicted[i]:
                            self.active_count += 1
                            self.inactive_count = 0
                        else:
                            self.active_count = 0

                        if self.active_count > self.active_thresh:
                            # start a new speech event
                            self.add_rows(self.speech_data, np.transpose(np.array(self.prev_data))[:, -5*self.skip:], 100) # previous 100 samples
                            self.add_rows(self.speech_data, curr_data, 20) # current 20 samples

                    # update prev
                    self.pop_prev(20)
                    self.add_rows(self.prev_data, curr_data, 20)




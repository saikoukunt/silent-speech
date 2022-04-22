# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 19:00:24 2022

@author: lwing
"""

import Boolean
import SAD_struct
import numpy as np
from collections import deque
import threading
import pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd

class SAD():
    def __init__(self):


        self.globalIsFinished = Boolean.boolean()

        #variables for determining speech event
        
        self.active_count = 0        #number of speech events
        self.inactive_count = 0
        self.active_thresh = 3
        self.inactive_thresh = 7
        self.isSpeech = Boolean.boolean()

        #number of samples per packet
        self.num_samples = 240

        #frame_length is in ms
        self.frame_length = 240
        
        
        
    def rms(self, raw):
        rms_window = deque([0,0,0,0,0])
        rms_data = np.zeros(len(raw))
        for i, sample in enumerate(raw):
            rms_window.popleft()
            rms_window.append(sample)
            val = np.sqrt(sum(np.square(rms_window)/5))
            rms_data[i] = val
            
        return rms_data
    
    

    def smooth(self, rms_data):
        
        #large window to average over; sampling rate is 1000 Hz; each sample is a millisecond
        window = 40
        
        #overlap interval
        skip = 20
        
        ind1 = 0
        ind2 = window
        #assuming that the packet size i.e. length of raw data and rms_data will be a multiple of 20
        downsampled = np.zeros(int(len(rms_data)/20)+1)
        i = 0
        while ind1 < len(rms_data):
                
            #remaining data less than window size, avoid array out of bounds
            if ind2 > len(rms_data):
                ind2 = len(rms_data)-1
                    
            val = np.mean(rms_data[ind1:ind2], dtype=np.float64)
            downsampled[i] = val
            ind1 = ind1 + skip
            ind2 = ind2 + skip
            i = i+1
                
        return downsampled


    def create_SpeechDataQueues(self):
        return [deque(),deque(),deque(),deque(),deque(),deque()]
    

    def global_thread(self, struct, output):
            
        
        clf = pickle.load(open("classifier.pkl", 'rb'))
        scaler = pickle.load(open("scaler.pkl", 'rb'))
        speech_data = self.create_SpeechDataQueues()
        
        while True:
            self.globalIsFinished.setStatus(False)
            
            #augment data, make a dataframe, predict on it, then send through fsm
            ready_data = np.zeros((6,12))
            
            for i in range(6):
                data_rms = self.rms(struct.getDataTableRow(i))
                res = self.smooth(data_rms)
                ready_data[i] = res
            
            df = pd.DataFrame({
                
                "Chan1": ready_data[0],
                "Chan2": ready_data[1],
                "Chan6": ready_data[5]
            })
            
            X = df[['Chan1', 'Chan2', 'Chan6']]
            
            X = scaler.transform(X)
            predicted = clf.predict(X)
            
            
            speech_event = np.zeros(12)
            
            
            for sample_idx in range(12):
                          
                if self.isSpeech.getStatus():
                    if not predicted[sample_idx]:
                        self.inactive_count += 1
                    else:
                        self.inactive_count = 0
                
                    if self.inactive_count > self.inactive_thresh:
                        self.isSpeech.setStatus(False)
                        speech_event[sample_idx] = 0
                    else:
                        self.isSpeech.setStatus(True)
                        speech_event[sample_idx] = 1
         
                else:
                    #updating speech event count
                    if predicted[sample_idx]:
                        self.active_count += 1
                    else:
                        self.active_count = 0
            
                    #Speech Event conditional
                    #test
                    if self.active_count > self.active_thresh:
                        self.isSpeech.setStatus(True)
                        speech_event[sample_idx] = 1
                            
                    else:
                        self.isSpeech.setStatus(False)
                        speech_event[sample_idx] = 0
                        
            
            for speech_sample_index, element in enumerate(speech_event):
                
                if element == 1:
                    for channel_index in range(6):
                        for raw_sample in range(20):
                            raw_index = int((20 * speech_sample_index)+raw_sample)
                            speech_data[channel_index].append(struct.getDataTableEntry(channel_index, raw_index))
                            
                else:
                    #6xsomething
                    output_array = np.array([speech_data[0], speech_data[1], speech_data[2], speech_data[3], speech_data[4], speech_data[5]])
                            
                    output.put(output_array)
                        
                    speech_data = self.create_SpeechDataQueues()
            
            self.globalIsFinished.setStatus(True)
            
            while self.globalIsFinished.getStatus():
                #do nothing until new data is sent
                pass



    def run(self, input, output):
        
        #240x6
        data_list = input.get()
        
        
        data_struct = SAD_struct.sad_struct(np.transpose(data_list),self.num_samples)
        
        global_thread = threading.Thread(target=self.global_thread, args=(data_struct,output))
        
        global_thread.start()
        
        
        while True:
            if self.globalIsFinished.getStatus():
                
                #data_list = getDataStream()
                #240x6
                data_list = input.get()
                
                
                data_struct.setDataTable(np.transpose(data_list))
                
                self.globalIsFinished.setStatus(False)        
        

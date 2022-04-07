# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 15:30:32 2022

@author: lwing
"""

from collections import deque
import numpy as np
from statistics import mean

class channel():
    def __init__(self, data, frame_length, channel_num):
        super().__init__()
    
        #frame_length is time
        self.data_rate = 1
        self.data_size = frame_length * self.data_rate
        self.active = False
        self.max_power = 0
        self.min_power= 0 
        self.max_thresh = 1
        self.min_thresh = 1
    
        self.raw_data = data.deque()
        self.prepped_data_frame = deque()
        self.channel_num = channel_num -1
        self.hasData = True
       
        
    def getData_Rate(self):
        return self.data_rate
    
    def setData_Rate(self, value):
        self.data_rate = value
        
    def getData_Size(self):
        return self.data_size
    
    def setData_Size(self, value):
        self.data_size = value
        
    def isActive(self):
        return self.active()
    
    def setActive(self, res):
        self.active = res
        
    def getMax_Power(self):
        return self.max_power
    
    def setMax_Power(self, value):
        self.max_power = value
    
    def getMin_Power(self):
        return self.min_power
    
    def setMin_Power(self, value):
        self.min_power = value
        
    def getMax_Thresh(self):
        return self.max_thresh
    
    def setMax_Thresh(self, value):
        self.max_thresh = value
        
    def getMin_Thresh(self):
        return self.min_thresh
    
    def setMin_Thresh(self, value):
        self.min_thresh = value
        
    def getRaw(self):
        return self.raw_data
    
    def setRaw(self, data):
        self.raw_data = data.deque()
    
    def getPrepped(self):
        return self.prepped_data_frame
    
    def getChannelNum(self):
        return self.channel_num
    
    def getHasData(self):
        return self.hasData
    
    def setHasData(self, value):
        self.hasData = value
        
      
    def rms(self, raw):
        rms_window = deque([0,0,0,0,0])
        rms_data = np.zeros(len(raw))
        for i, sample in enumerate(raw):
            rms_window.popleft()
            rms_window.append(sample)
            val = np.sqrt(sum(np.square(rms_window)/5))
            rms_data[i] = val
        
        return rms_data
    
    
    #TO DO: MAKE SURE ARRAY OUT OF BOUNDS CHECK IS SUFFICIENT
    def smooth(self, rms_data):
        
        #large window to average over; sampling rate is 1000 Hz; each sample is a millisecond
        window = 40
        
        #overlap interval
        skip = 20
        
        ind1 = 0
        ind2 = window
        #assuming that the packet size i.e. length of raw data and rms_data will be a multiple of 20
        downsampled = np.zeros(int(len(rms_data)/20))
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
        
    def calculate(self, smoothed_envelope):
        
        return np.abs(np.diff(smoothed_envelope))
    
    def create_dataFrame(self):
        #downsampled version so len is 1/20 raw len
        self.prepped_data_frame = deque(self.calculate(self.smooth(self.rms((self.raw_data)))))
    
    def inactivity_check(self):
        sample = self.prepped_data_frame.leftpop()
        
        if self.active:
            if sample > (self.max_power * self.max_thresh):
                self.active = True
            else:
                self.active = False
            if sample > self.max_power:
                self.max_power = sample
            
            
        else:
            if sample < (self.min_power * self.min_thresh):
                self.active = False
            else:
                self.active = True
            if sample < self.min_power:
                self.min_power = sample
            
            
        
        
        
        
        
        
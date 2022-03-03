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
        self.prepped_data_frame
        self.channel_num = channel_num
       
        
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
    
    def getPrepped(self):
        return self.prepped_data_frame
    
    def getChannelNum(self):
        return self.channel_num
        
      
    #TO DO: MAKE SURE ARRAY OUT OF BOUNDS CHECK IS SUFFICIENT
    def smooth(self, raw):
        
        #large window to average over
        window = int(self.data_rate * 40)
        
        #overlap interval
        skip = int(self.data_rate * 20)
        
        ind1 = 0
        ind2 = window
        copy = np.copy(np.array(raw))
        
        while ind1 < self.data_size:
            
            #remaining data less than window size, avoid array out of bounds
            if ind2 > self.data_size:
                ind2 = int(self.data_size)
                
            val = mean(copy[ind1:ind2])
            copy[ind1:ind2] = val
            ind1 = ind1 + skip
            ind2 = ind2 + skip
            
        return copy
        
        
    def calculate(self, smoothed_envelope):
        
        return np.abs(np.diff(smoothed_envelope))
    
    def create_dataFrame(self):
        self.prepped_data_frame = deque(self.calculate(self.smooth(self.raw_data)))
    
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
            
            
        
        
        
        
        
        
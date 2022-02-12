# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 15:30:32 2022

@author: lwing
"""

from collections import deque
import numpy as np
from statistics import mean

class channel():
    def __init__(self, data, frame_length):
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
       
        
        
    #TO DO: MAKE SURE ARRAY OUT OF BOUNDS CHECK IS SUFFICIENT
    def smooth(self, raw):
        raw = list(raw)
        
        #large window to average over
        window = int(self.data_rate * 40)
        
        #overlap interval
        skip = int(self.data_rate * 20)
        
        ind1 = 0
        ind2 = window
        raw = np.array(raw)
        
        while ind1 < self.data_size:
            
            #remaining data less than window size, avoid array out of bounds
            if ind2 > self.data_size:
                ind2 = int(self.data_size)
                
            val = mean(raw[ind1:ind2])
            raw[ind1:ind2] = val
            ind1 = ind1 + skip
            ind2 = ind2 + skip
            
        raw = raw.tolist()
        return raw
        
        
    def calculate(self, smoothed_envelope):
        smoothed = list(smoothed_envelope)
        return np.abs(np.diff(smoothed))
    
    def inactivity_check(self):
        data_frame = deque(self.calculate(self.smooth(self.raw_data)))
        frame = data_frame.leftpop()
        
        if self.active:
            if frame > (self.max_power * self.max_thresh):
                self.active = True
            else:
                self.active = False
            if frame > self.max_power:
                self.max_power = frame
            
            
        else:
            if frame < (self.min_power * self.min_thresh):
                self.active = False
            else:
                self.active = True
            if frame < self.min_power:
                self.min_power = frame
            
            
        
        
        
        
        
        
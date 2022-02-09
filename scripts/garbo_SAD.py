# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 15:30:32 2022

@author: lwing
"""

from collections import deque
import numpy as np

class channel(self,  data, int frame_length):
    
    #frame_length is time
    self.data_rate = 1
    self.data_size = frame_length * data_rate
    self.active = False
    self.max_power = 0
    self.min_power= 0 
    self.max_thresh = 1
    self.min_thresh = 1
    
    raw_data = data.deque()
    
    
    
    def smooth(self):
        
    def calculate(self, smoothed_envelope):
        smoothed = list(smoothed_envelope)
        return np.abs(np.diff(smoothed))
    
    def inactivity_check(self):
        data_frame = deque(calculate(smooth(raw_data)))
        frame = data_frame.leftpop()
        
        if self.active:
            if frame > (max_power * max_thresh):
                self.active = True
            else:
                self.active = False
            if frame > max_power:
                max_power = frame
            
            
        else:
            if frame < (min_power * min_thresh):
                self.active = False
            else:
                self.active = True
            if frame < min_power:
                min_power = frame
            
        
        
        
        
        
        
        
        
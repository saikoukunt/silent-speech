# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 16:21:45 2022

@author: lwing
"""

import garbo_SAD
import numpy as np
from collections import deque
import threading



#global count of active channels

active_channels = 0

#frame_length is in ms
frame_length = 80


channel = garbo_SAD.channel(data_stream, frame_length)
def channel_thread(channel, lock):
    while True:
        channel.inactivity_check()
        result = channel.isActive()
    
    
    

def controller_thread(lock)
    


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
    
    global active_channels
    
    while True:
        channel.inactivity_check()
        result = channel.isActive()
        
        
        
        #NEED SOME OTHER METHOD FOR TRACKING NUMBER OF ACTIVE CHANNELS
        lock.acquire()
        if result:
            active_channels = active_channels + 1
        else:
            active_channels = active_channels - 1
        lock.release()
    
    
    

def controller_thread():
    
    global active_channels
    active_channels = 0
    channel1 = garbo_SAD.channel(data_stream1, frame_length)
    channel2 = garbo_SAD.channel(data_stream2, frame_length)
    channel3 = garbo_SAD.channel(data_stream3, frame_length)
    channel4 = garbo_SAD.channel(data_stream4, frame_length)
    channel5 = garbo_SAD.channel(data_stream5, frame_length)
    channel6 = garbo_SAD.channel(data_stream6, frame_length)
    
    lock = threading.Lock()
  
    # creating threads
    t1 = threading.Thread(target=channel_thread, args=(channel1, lock,))
    t2 = threading.Thread(target=channel_thread, args=(channel2, lock,)) 
    t3 = threading.Thread(target=channel_thread, args=(channel3, lock,))
    t4 = threading.Thread(target=channel_thread, args=(channel4, lock,)) 
    t5 = threading.Thread(target=channel_thread, args=(channel5, lock,))
    t6 = threading.Thread(target=channel_thread, args=(channel6, lock,)) 

    

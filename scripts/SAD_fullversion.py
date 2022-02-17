# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 16:21:45 2022

@author: lwing
"""

import garbo_SAD
import numpy as np
from collections import deque
import threading



#global boolean for each channel
chan1_active = False
chan2_active = False
chan3_active = False
chan4_active = False
chan5_active = False
chan6_active = False

#variables for determining speech event
num_active = 0          #number of active channels for a single cycle
num_inactive = 0
active_count = 0        #number of speech events
inactive_count = 0
active_thresh = 3
inactive_thresh = 2
isSpeech = False

#frame_length is in ms
frame_length = 80


def channel_thread(channel, boolean):
       
        channel.inactivity_check()
        boolean = channel.isActive()
        

def controller_thread(data_list):
    
    data_stream1 = data_list[0]
    data_stream2 = data_list[1]
    data_stream3 = data_list[2]
    data_stream4 = data_list[3]
    data_stream5 = data_list[4]
    data_stream6 = data_list[5]
    
    channel1 = garbo_SAD.channel(data_stream1, frame_length)
    channel2 = garbo_SAD.channel(data_stream2, frame_length)
    channel3 = garbo_SAD.channel(data_stream3, frame_length)
    channel4 = garbo_SAD.channel(data_stream4, frame_length)
    channel5 = garbo_SAD.channel(data_stream5, frame_length)
    channel6 = garbo_SAD.channel(data_stream6, frame_length)
    
  
    # creating threads
    t1 = threading.Thread(target=channel_thread, args=(channel1, chan1_active,))
    t2 = threading.Thread(target=channel_thread, args=(channel2, chan2_active,)) 
    t3 = threading.Thread(target=channel_thread, args=(channel3, chan3_active,))
    t4 = threading.Thread(target=channel_thread, args=(channel4, chan4_active,)) 
    t5 = threading.Thread(target=channel_thread, args=(channel5, chan5_active,))
    t6 = threading.Thread(target=channel_thread, args=(channel6, chan6_active,))
    
    threads = [t1, t2, t3, t4, t5, t6]
    
    #starting threads
    for t in threads:
        t.start()
    
    #joining threads
    for t in threads:
        t.join()

    #global boolean logic check
    channels = [chan1_active, chan2_active, chan3_active, chan4_active, chan5_active, chan6_active]
    count = 0
    for chan in channels:
        if chan:
            count = count + 1
    num_active = count
    
    
    #Speech Event FSM
    if isSpeech:
        if num_active < 2:
            inactive_count += 1
        else:
            inactive_count = 0
            
        if inactive_count >= inactive_thresh:
            isSpeech = False
        else:
            isSpeech = True
     
        
    else:
        #updating speech event count
        if num_active >= 2:
            active_count += 1
        else:
            active_count = 0
        
        #Speech Event conditional
        if active_count >= active_thresh:
            isSpeech = True
        else:
            isSpeech = False
            
            
            
def main_task():
    #leaving blank for now, controller_thread assumes a list of deques
    data = getDataStream()
    
    '''
    manipulate data from "getDataStream"
    
    '''
    controller = threading.Thread(target=controller_thread, args=(data,))
    controller.start()
    controller.join()
        

if __name__ == "__main__":
    
    while True:
        main_task()
        
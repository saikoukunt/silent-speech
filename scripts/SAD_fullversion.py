# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 16:21:45 2022

@author: lwing
"""

import Boolean
import garbo_SAD
import SAD_struct
import numpy as np
from collections import deque
import threading



#global boolean for each channel
chan1_active = Boolean.boolean()
chan2_active = Boolean.boolean()
chan3_active = Boolean.boolean()
chan4_active = Boolean.boolean()
chan5_active = Boolean.boolean()
chan6_active = Boolean.boolean()

globalIsFinished = Boolean.boolean()

#variables for determining speech event
num_active = 0          #number of active channels for a single cycle
num_inactive = 0
active_count = 0        #number of speech events
inactive_count = 0
active_thresh = 3
inactive_thresh = 2
isSpeech = Boolean.boolean()

#number of samples per packet
num_samples = 1

#frame_length is in ms
frame_length = 80

#Each channel has access to the 'packet' struct which contains all 6 channels'
#raw data as well as an array of booleans for channel activity
#The global thread will poll over the struct's boolean_table to determine when
#speech events occur
#After a string of raw data has been fully processed, the channel thread will
#wait indefinitely until it gets a new data set to process
def channel_thread(channel, boolean, struct):
    while True:
        channel.setHasData(True)
        active_flag_curr = False
        channel.create_dataFrame()
        for sample_idx in range(num_samples):
            channel.inactivity_check()
            active_flag_curr = channel.isActive()
            
            #1 in the boolean table will represent true
            if active_flag_curr:
                struct.setBooleanTableEntry(channel.getChannelNum(),sample_idx, 1)
                boolean.setStatus(True)
            
            #-1 in the boolean table will represent false
            else:
                struct.setBooleanTableEntry(channel.getChannelNum(),sample_idx, -1)
                boolean.setStatus(False)
        
        channel.setHasData(False)    
        while not channel.getHasData():
            pass
            #do nothing, waiting for new raw data
            
def create_SpeechDataQueues():
    return [deque(),deque(),deque(),deque(),deque(),deque()]


def global_thread(struct):
    while True:
        globalIsFinished.setStatus(False)
        speech_data = create_SpeechDataQueues()
        
        for sample_idx in range(num_samples):
            
            #waiting for each channel to finish its inactivity check on the current sample
            while (np.count_nonzero(struct.getBooleanTable()[:,sample_idx] == 1) + np.count_nonzero(struct.getBooleanTable()[:,sample_idx] == -1)) < 6 :
                pass
                #do nothing
            
            num_active = np.count_nonzero(struct.getBooleanTable()[:,sample_idx] == 1)   
            
            if isSpeech.getStatus():
                if num_active < 2:
                    inactive_count += 1
                else:
                    inactive_count = 0
            
                if inactive_count >= inactive_thresh:
                    isSpeech.setStatus(False)
                    
                    '''
                    
                    send data in speech_data to next module
                    
                    '''
                    speech_data = create_SpeechDataQueues()
                    
                else:
                    isSpeech.setStatus(True)
                    for idx, queue in enumerate(speech_data):
                        queue.append(struct.getDataTableEntry(idx, sample_idx))
     
        
            else:
                #updating speech event count
                if num_active >= 2:
                    active_count += 1
                else:
                    active_count = 0
        
                #Speech Event conditional
                if active_count >= active_thresh:
                    isSpeech.setStatus(True)
                    for idx, queue in enumerate(speech_data):
                        queue.append(struct.getDataTableEntry(idx, sample_idx))
                        
                else:
                    isSpeech.setStatus(False)
                    
        globalIsFinished.setStatus(True)
        struct.createBooleanTable()             #resetting boolean table
        
        while globalIsFinished.getStatus():
            #do nothing until new data is sent
            pass    
'''
TO DO:
    Initial struct creation
    Handle new data passing into global and channel threads
    Initial thread creation

'''
        

if __name__ == "__main__":
    
    data_list = getDataStream()
    
    '''
    manipulate data from "getDataStream"
    
    '''
    
    data_stream1 = data_list[0]
    data_stream2 = data_list[1]
    data_stream3 = data_list[2]
    data_stream4 = data_list[3]
    data_stream5 = data_list[4]
    data_stream6 = data_list[5]
    
    channel1 = garbo_SAD.channel(data_stream1, frame_length, 1)
    channel2 = garbo_SAD.channel(data_stream2, frame_length, 2)
    channel3 = garbo_SAD.channel(data_stream3, frame_length, 3)
    channel4 = garbo_SAD.channel(data_stream4, frame_length, 4)
    channel5 = garbo_SAD.channel(data_stream5, frame_length, 5)
    channel6 = garbo_SAD.channel(data_stream6, frame_length, 6)
    
    data_struct = SAD_struct.sad_struct(data_list,num_samples)
    
    t1 = threading.Thread(target=channel_thread, args=(channel1, chan1_active, data_struct))
    t2 = threading.Thread(target=channel_thread, args=(channel2, chan2_active, data_struct)) 
    t3 = threading.Thread(target=channel_thread, args=(channel3, chan3_active, data_struct))
    t4 = threading.Thread(target=channel_thread, args=(channel4, chan4_active, data_struct)) 
    t5 = threading.Thread(target=channel_thread, args=(channel5, chan5_active, data_struct))
    t6 = threading.Thread(target=channel_thread, args=(channel6, chan6_active, data_struct))
    global_thread = threading.Thread(target=global_thread, args=(data_struct,))
    
    
    threads = [t1, t2, t3, t4, t5, t6, global_thread]
    
    #starting threads
    for t in threads:
        t.start()
    
    while True:
        if globalIsFinished.getStatus():
            
            data_list = getDataStream()
            '''
            manipulate data from "getDataStream"
    
            '''
            data_struct.setDataTable(data_list)
            
            channel1.setRaw(data_list[0])
            channel2.setRaw(data_list[1])
            channel3.setRaw(data_list[2])
            channel4.setRaw(data_list[3])
            channel5.setRaw(data_list[4])
            channel6.setRaw(data_list[5])
            
            channel1.setHasData(True)
            channel2.setHasData(True)
            channel3.setHasData(True)
            channel4.setHasData(True)
            channel5.setHasData(True)
            channel6.setHasData(True)
            
            globalIsFinished.setStatus(False)
            
            
            
            
            
            
            
            
            
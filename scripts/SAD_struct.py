# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 11:57:14 2022

@author: lwing
"""

#Goal here is to have one object that the global thread can poll over rather
#than pulling information from a bunch of separate threads
import numpy as np

class sad_struct():
    def __init__(self, big_data_array, num_samples):
        super().__init__()
        
        self.num_samples = num_samples
        
        #array of arrays holding all the channels' raw data
        self.data_table = big_data_array
        
        #boolean table for global to poll over for speech events
        self.boolean_table = np.zeros([6,self.num_samples/20])
        
    
    def setBooleanTableEntry(self, channel, sample_index, val):
        self.boolean_table[channel, sample_index] = val
    
    def setDataTable(self, data_array):
        self.data_table = data_array
        
    def createBooleanTable(self):
        self.boolean_table = np.zeros([6,self.num_samples/20])
    
    def getDataTable(self):
        return self.data_table
    
    def getDataTableEntry(self, channel, sample_index):
        return self.data_table[channel, sample_index]
    
    def getBooleanTable(self):
        return self.boolean_table
    
    def getBooleanTableRow(self, row):
        return self.boolean_table[row,:]
    
    def getBooleanTableCol(self, col):
        return self.boolean_table[:, col]
        
    def getBooleanTableEntry(self, channel, sample_index):
        return self.boolean_table[channel, sample_index]
        
        
     
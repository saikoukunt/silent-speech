# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 14:21:28 2022

@author: lwing
"""

class boolean():
    def __init__(self):
        super().__init__()
        
        self.status = False
        
    def getStatus(self):
        return self.status
    
    def setStatus(self, val):
        self.status = val
        
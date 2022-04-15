import numpy as np
import matplotlib.pyplot as plt
from extract_data import extract_data

data, words, starts, ends = extract_data("../data/single_binary.txt","../data/single_binary_times.txt")

plt.figure(figsize=(20,8))
for i in range(6):
    plt.subplot(6,1,i+1)
    plt.plot(data[:,i]); plt.ylim(plt.ylim())
    plt.vlines(starts,-2,2,'g'); plt.vlines(ends,-2,2,'r')

plt.tight_layout()
plt.show()
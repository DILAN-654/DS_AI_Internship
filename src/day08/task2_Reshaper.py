# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 12:02:23 2026

@author: dilan
"""

import numpy as np

data = np.arange(24)
print("Original 1D Array:")
print(data)
print("Shape:", data.shape)

reshaped_data = data.reshape(4, 3, 2)
print("\nReshaped Array (4, 3, 2):")
print(reshaped_data)
print("Shape:", reshaped_data.shape)

transposed_data = reshaped_data.transpose(0, 2, 1)

print("\nFinal Transposed Array:")
print(transposed_data)
print("Final Shape:", transposed_data.shape)

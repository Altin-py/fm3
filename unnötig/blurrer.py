#!/usr/bin/env python3
"""
"""
from skimage.filters import gaussian
def blurrer(Data_clear, sigma):
    Data_blurr = gaussian(
    Data_clear, sigma=(sigma, sigma), truncate=3.5, multichannel=False)
    return Data_blurr

#!/usr/bin/env python3
"""
"""
import numpy as np
from skimage.filters import laplace
from scipy import ndimage
from scipy.fftpack import fft2
def M123(Data):
    M0 = np.sum(abs(fft2(Data)))
    M1 = np.sum(abs(fft2(Data))**2)
    M2 = np.sum(abs(ndimage.sobel(Data))**2)
    M3 = np.sum(abs(laplace(Data))**2)
    Ms = laplace(Data).var()
    return M0, M1, M2, M3, Ms

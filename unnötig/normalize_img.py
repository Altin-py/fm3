#!/usr/bin/env python3
"""
"""
import cv2
import numpy as np
def normalize_img(data):
    dst = np.zeros(data.shape)
    final_img = cv2.normalize(data, dst, 2 , 255, norm_type=cv2.NORM_MINMAX)
    return final_img


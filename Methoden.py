#!/usr/bin/env python3
"""
"""
import numpy as np
from skimage.filters import laplace, gaussian
from scipy import ndimage
from scipy.fftpack import fft2
from math import atan2, cos, sin, sqrt, pi
from skimage.feature import canny
import cv2
import pickle
import os

def M123(Data):
    M0 = np.sum(abs(fft2(Data)))
    M1 = np.sum(abs(fft2(Data))**2)
    M2 = np.sum(abs(ndimage.sobel(Data))**2)
    M3 = np.sum(abs(laplace(Data))**2)
    Ms = laplace(Data).var()
    return M0, M1, M2, M3, Ms

def normalize_img(data):
    dst = np.zeros(data.shape)
    final_img = cv2.normalize(data, dst, 2 , 255, norm_type=cv2.NORM_MINMAX)
    return final_img


def reading(inp):
    dir_path = os.path.dirname(os.path.realpath('__file__')) # in diesem Fall sollten die Bilder im gleichen Ordner wie die das Skript liegen
    infile = open(inp, 'rb')
    Data = pickle.load(infile)
    infile.close()
    return Data


def blurrer(Data_clear, sigma):
    Data_blurr = gaussian(
    Data_clear, sigma=(sigma, sigma), truncate=3.5, multichannel=False)
    return Data_blurr


def remove_background(img, over_SP, under_SP, dilate_edge=2, erode_bg=5, crop_px=4):
    """ Removes faulty pixels and background
    Only works if rotation is not too strong - seedPoints must be background.
    @param img: 2d-array
        dilate_edge: size of kernel for dilation of edges
        erode_bg: size of kernel for erosion of background
        crop_px: even integer, how much the image is cropped in width and height combined
    """
    # Salt-and-pepper noise entfernen
    img = cv2.medianBlur(img.astype(np.float32), 3)
    # Bild in 8-Bit-verträglichen Wertebereich bringen (für Canny)
    # 255*..., stattdessen 250*.. sodass 255 nicht angenommen wird
    img_8bit = 250 * ((img - np.min(img)) / (np.max(img) - np.min(img)))
    img_8bit = smooth_image(img_8bit)
    canny_img = cv2.Canny(img_8bit.astype(np.uint8), 0.05 * 255, 0.15 * 255, L2gradient=True)
    # Fill gaps in edge or double edges
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (dilate_edge, dilate_edge))
    canny_img = cv2.dilate(canny_img, kernel)
    # Mask must be 2px larger in each direction
    mask = cv2.copyMakeBorder(canny_img, 1, 1, 1, 1, cv2.BORDER_REFLECT)
    # To avoid black gaps at the border, cut 2px off the images
    mask = mask[int(crop_px/2):mask.shape[0] - int(crop_px/2), int(crop_px/2):mask.shape[1] - int(crop_px/2)]
    img_8bit = img_8bit[int(crop_px/2):img_8bit.shape[0] - int(crop_px/2), int(crop_px/2):img_8bit.shape[1] - int(crop_px/2)]
    height = img_8bit.shape[0]
    width = img_8bit.shape[1]

    # Floodfill ueber Rotorblatt
    ret, img_filled, mask, rect = cv2.floodFill(img_8bit, mask.astype(np.uint8), loDiff=20, upDiff=20,
                                                seedPoint=eval(over_SP),
                                                newVal=0, flags=4 | (255 << 8))
    # Floodfill unter Rotorblatt
    ret, img_filled, mask, rect = cv2.floodFill(img_8bit, mask.astype(np.uint8), loDiff=20, upDiff=20,
                                                seedPoint=eval(under_SP),
                                                newVal=0, flags=4 | (255 << 8))

    # Erosion to fill in gaps in background
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (erode_bg, erode_bg))
    img_corr = cv2.erode(img_8bit, kernel)

    # Values of img_corr are modified and will not be returned; use img_corr as mask for img
    img = img[int(crop_px/2):img.shape[0] - int(crop_px/2), int(crop_px/2):img.shape[1] - int(crop_px/2)]
    img_no_bg = cv2.copyTo(img, img_corr.astype(np.uint8))
    # Remove strongly negative values (should be background)
    img_no_bg = np.where(img_no_bg < -5, 0, img_no_bg)
    return img_no_bg

def smooth_image(data):
    """ Ein Bild mit einem Filter glätten """
    # data = cv2.GaussianBlur(data, (5, 5), cv2.BORDER_DEFAULT)
    return cv2.bilateralFilter(data.astype(np.float32), 5, 35, 75)  # Besser als GaussianBlur um Kanten zu erhalten


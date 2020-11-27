#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 17:38:15 2020

@author: altin
Provided input Data function will determine focus measure 0,1,3 for a gaussian noise filtered image with constant sigma. For sigma = 0 the focus measure is set to one by default.

"""

_DESCRIPTION = '''Plots the data and compares focus measures of 3 different gaussian blurr values'''
import matplotlib.pyplot as plt
import numpy as np
import argparse
import sys
from scipy.fftpack import fft2, ifft2
from skimage.filters import gaussian, laplace
import os
import pickle
dir_path = os.path.dirname(os.path.realpath('__file__')) # in diesem Fall sollten die Bilder im gleichen Ordner wie die das Skript liegen
infile = open('Bilder', 'rb')
Data = pickle.load(infile)
infile.close()


def main(): #positional arguments not yet used, summing over everything
    """
    args: 

    imageid: int number to select from set of data
    sigma: float number to determine how wide the gaussian filter is
    x1,x2,y1,y2: positional arguments of the included pixels integet number

    returns:

    non filtered image and filtered image with computed focus measure M0,M1,M3
    """
    ################################################################
    ################Parsing Arguments###############################
    args= _parse_arguments()
    print(args)
    imageid = args.id
    sigma1 = float(args.sig1)
    sigma2 = float(args.sig2)
    sigma3 = float(args.sig3)

    ################################################################
    Data_clear = Data[imageid]


    Data_blurr1 = gaussian(
    Data_clear, sigma=(sigma1, sigma1), truncate=3.5, multichannel=False)

    M0_clear = np.sum(abs(fft2(Data_clear)))
    M1_clear = np.sum(abs(fft2(Data_clear))**2)
    M3_clear = np.sum(abs(laplace(Data_clear))**2)


    M0_blurr = np.sum(abs(fft2(Data_blurr1))) 
    M1_blurr = np.sum(abs(fft2(Data_blurr1))**2)
    M3_blurr = np.sum(abs(laplace(Data_blurr1))**2)


    VERG1 = [M0_blurr/M0_clear, M1_blurr/M1_clear, M3_blurr/M3_clear]
    print(VERG1)


    Data_blurr2 = gaussian(
    Data_clear, sigma=(sigma2, sigma2), truncate=3.5, multichannel=False)


    M0_blurr = np.sum(abs(fft2(Data_blurr2)))
    M1_blurr = np.sum(abs(fft2(Data_blurr2))**2)
    M3_blurr = np.sum(abs(laplace(Data_blurr2))**2)

    VERG2 = [M0_blurr/M0_clear, M1_blurr/M1_clear, M3_blurr/M3_clear]
    print(VERG2)


    Data_blurr3 = gaussian(
    Data_clear, sigma=(sigma3, sigma3), truncate=3.5, multichannel=False)

    M0_blurr = np.sum(abs(fft2(Data_blurr3)))
    M1_blurr = np.sum(abs(fft2(Data_blurr3))**2)
    M3_blurr = np.sum(abs(laplace(Data_blurr3))**2)


    VERG3 = [M0_blurr/M0_clear, M1_blurr/M1_clear, M3_blurr/M3_clear]
    print(VERG2)



    f = plt.figure()
    t1 = f.add_subplot(231)
    t1.title.set_text('Scharfes Bild Nr.' + str(imageid))
    t1.axis('off')
    plt.imshow(Data_clear)

    t2 = f.add_subplot(232)
    t2.title.set_text('Laplace Filter')
    t2.axis('off')
    plt.imshow(laplace(Data_clear))

    t3 = f.add_subplot(233)
    t3.title.set_text('FFT')
    t3.axis('off')
    plt.imshow(abs(fft2(Data_clear)))


    t4 = f.add_subplot(234)
    t4.title.set_text('s1 = ' + str(sigma1) + ' M0=' + str(round(VERG1[0],4)) + '\n  M1 = ' + str(round(VERG1[1],4))+ ' M3 = ' + str(round(VERG1[2],4)))
    t4.axis('off')
    plt.imshow(Data_blurr1)

    t5 = f.add_subplot(235)
    t5.title.set_text('s2 = ' + str(sigma2) + ' M0=' + str(round(VERG2[0],4)) + '\n  M1 = ' + str(round(VERG2[1],4))+ ' M3 = ' + str(round(VERG2[2],4)))
    t5.axis('off')
    plt.imshow(Data_blurr2)

    t6 = f.add_subplot(236)
    t6.title.set_text('s3 = ' + str(sigma3) + ' M0=' + str(round(VERG3[0],4)) + '\n  M1 = ' + str(round(VERG3[1],4))+ 'M3 = ' + str(round(VERG3[2],4)))
    t6.axis('off')
    plt.imshow(Data_blurr3)

    f.set_figheight(15)
    f.set_figwidth(15)
    plt.show(block=True)

def _parse_arguments():
    parser = argparse.ArgumentParser(description=_DESCRIPTION)

    msg = 'Directory, where input file is located and where output should be'\
        ' written to (default: .)'
    parser.add_argument('-d', metavar='DIR', default='.', help=msg)

    msg = 'State desired title of figure'
    parser.add_argument('-t',default=None, help=msg)

    msg = 'Index of Image from 0 to 8 '
    parser.add_argument('-id',default=0, help=msg)

    msg = 'First Value of blurr '
    parser.add_argument('-sig1',default=0.2, help=msg)

    msg = 'Second Value of blurr '
    parser.add_argument('-sig2',default=0.5, help=msg)

    msg = 'Third Value of blurr '
    parser.add_argument('-sig3',default=1.5, help=msg)



    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main() 

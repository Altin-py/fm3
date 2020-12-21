#!/usr/bin/env python3

import matplotlib.pyplot as plt
from Methoden import reading
from Methoden import remove_background as rmbg
from Methoden import normalize_img as nimg

def main():
    """
    """
    Data = reading('Bilder')
    
    for jj in range(9):
        Data_clearcut = rmbg(Data[jj],"(100,0)",str((100,500)))
        Data_clearcut = nimg(Data_clearcut)
        jj = str(jj)
        f = plt.figure()
        plt.title("Bild" + jj)
        plt.imshow(Data_clearcut)
        plt.savefig(jj +".png")


if __name__ == '__main__':
    main()

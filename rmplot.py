#!/usr/bin/env python3

import matplotlib.pyplot as plt
from reading import reading
from remove_background import remove_background as rmbg

def main():
    """
    """
    Data = reading('Bilder')
    
    for jj in range(9):
        Data_clearcut = rmbg(Data[jj],"(100,0)",str((100,500)))
        jj = str(jj)
        f = plt.figure()
        plt.imshow(Data_clearcut)
        plt.savefig(jj +".png")


if __name__ == '__main__':
    main()

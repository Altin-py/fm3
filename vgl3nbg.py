#!/usr/bin/env python3
"""
"""
import pandas as pd
from Methoden import reading
from Methoden import remove_background as rmbg
from Methoden import M123
from tabulate import tabulate

def main():
    """
    """
    Data = reading('Bilder')
    M0arr = []
    M1arr = []
    M2arr = []
    M3arr = []
    Msarr = []
    for jj in range(9):
        M0, M1, M2, M3, Ms = M123(rmbg(Data[jj],"(100,0)",str((100,500))))
        M0arr.append(M0)
        M1arr.append(M1)
        M2arr.append(M2)
        M3arr.append(M3)
        Msarr.append(Ms)
    M0 = M0arr/max(M0arr)
    M1 = M1arr/max(M1arr)
    M2 = M2arr/max(M2arr)
    M3 = M3arr/max(M3arr)
    Ms = Msarr/max(Msarr)

    #df = pd.DataFrame(list(zip(M0, M1, M2, M3, Ms)), index =['Bild 0', 'Bild 1', 'Bild 2', 'Bild 3', 'Bild 4', 'Bild 5', 'Bild 6', 'Bild 7', 'Bild 8'], 
                                              #columns =['M0', 'M1', 'M2', 'M3', 'Ms']) 
    df = pd.DataFrame(list(zip(M0, M1, M2, M3)), index =['Bild 0', 'Bild 1', 'Bild 2', 'Bild 3', 'Bild 4', 'Bild 5', 'Bild 6', 'Bild 7', 'Bild 8'], 
                                              columns =['M0', 'M1', 'M2', 'M3']) 
    print(tabulate(df, headers='keys', tablefmt='psql'))


if __name__ == '__main__':
    main()

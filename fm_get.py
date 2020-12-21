#!/usr/bin/env python3
"""
"""
_DESCRIPTION = '''Computes values of FM and writes them into csv. Compares 2 last values to indicate improvement in focus'''
import pandas as pd
import argparse
from csv import writer
from Methoden import reading as rd
from Methoden import M123
from Methoden import normalize_img as nimg
from Methoden import remove_background as rmbg

def main():
    args= _parse_arguments()
    ind = int(args.ind)


    Data = rd('Bilder')
    Data = nimg(rmbg(Data[ind],"(100,0)",str((100,500))))  #Hintergrund entfernt, histogramm normalisiert


    M0, M1, M2, M3, Ms = M123(Data)
    list_of_elem = [M0, M1, M2, M3]
    append_list_as_row("Messwerte.csv", list_of_elem)
    lines = length_list()-1
    anweisung_fokus(lines)

def _parse_arguments():
    parser = argparse.ArgumentParser(description=_DESCRIPTION)

    msg = 'Index of Image from 0 to 8 '
    parser.add_argument('-ind',default=0, help=msg)

    args = parser.parse_args()
    return args

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

def anweisung_fokus(ll, FM = 2):
    with open("Messwerte.csv", "r") as csvfile:
        data_txt = csvfile.read().splitlines()
    x=float(data_txt[-1].split(",")[FM])    
    y=float(data_txt[-2].split(",")[FM])
    if x/y > 1:
        print("Der Fokus hat sich verbessert")
    if x/y < 1:
        print("Der Fokus hat sich verschlechtert")
    if x/y == 1:
        print("Der Fokus ist gleich geblieben") 

def length_list(title = "Messwerte.csv"):
    with open("Messwerte.csv", "r") as csvfile:
        reader=csvfile.read()
    lines= len(list(reader))
    return lines

if __name__ == '__main__':
    main()

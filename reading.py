#!/usr/bin/env python3
import pickle
import os
def reading(inp):
    dir_path = os.path.dirname(os.path.realpath('__file__')) # in diesem Fall sollten die Bilder im gleichen Ordner wie die das Skript liegen
    infile = open(inp, 'rb')
    Data = pickle.load(infile)
    infile.close()
    return Data

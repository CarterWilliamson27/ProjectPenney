import os
import numpy as np
import time

def read_npy_file(name: str) -> list: # return unused data so python doesn't cheat and not actually read the file
    path = os.path.join('testing', 'data', 'npydata', name)
    data = np.load(path)
    zeroes = 0
    ones = 0
    for deck in data:
        for card in deck:
            if card == 0:
                zeroes += 1
            else:
                ones += 1
    return [zeroes, ones]

def read_bin_file(name: str) -> list: # return unused data so python doesn't cheat and not actually read the file
    path = os.path.join('testing', 'data', 'bindata', name)
    zeroes = 0
    ones = 0
    with open(path, 'rb') as file:
        for deck in file:
            for card in deck:
                if card == 0:
                    zeroes += 1
                else:
                    ones += 1
    return [zeroes, ones]

def test_read_data(isBinData: bool) -> list: 
    # test read speeds
    read_data = []
    if isBinData:
        files = os.listdir(os.path.join('testing', 'data', 'bindata'))
        for file in files:
            t0 = time.time()
            read_bin_file(file)
            t1 = time.time()
            read_data.append(t1-t0)
    else: 
        files = os.listdir(os.path.join('testing', 'data', 'npydata'))
        for file in files:
            t0 = time.time()
            read_npy_file(file)
            t1 = time.time()
            read_data.append(t1-t0)
    
    return read_data

    
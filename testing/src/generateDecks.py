import os
import numpy as np
import time

HALF_DECK = 26
NUM_DECKS_FILE = 10000

# Method 1: np.array with dtype u1 (Inspired by what Ron does)
def makeDecks(num_decks: int) -> list:
    random_seed = 0 # Base value, increased with each batch of decks
    loop_data = []
    write_data = []

    zeros = np.zeros(shape=HALF_DECK, dtype='u1')
    ones = np.ones(shape=HALF_DECK, dtype='u1')
    orig_deck = np.concatenate((zeros, ones))

    num_files = int(np.ceil(num_decks/NUM_DECKS_FILE)) # Calculate how many files we will need,
    # handles cases when 15000 decks are requested, etc.

    for _ in range(num_files):
        decks = []
        random_seed+=1
        np.random.seed(random_seed) # Set random seed for shuffling this batch of decks

        t0 = time.time()
        # Measure how long this loop takes to run
        for __ in range(NUM_DECKS_FILE):
            temp_deck = orig_deck.copy()
            np.random.shuffle(temp_deck)
            decks.append(temp_deck)

        t1 = time.time()
        loop_data.append(t1-t0)

        name =f'deck_{random_seed}_{len(decks)}.npy' # Save file as deck_randomseed_numdecks
        path = os.path.join('testing', 'data', 'npydata', name)

        t2 = time.time()
        # Measure how long it takes to write data to file
        np.save(path, decks)
        t3 = time.time()
        
        write_data.append(t3-t2)

    # return list of time data
    return [loop_data, write_data]


# Method 2: convert np.array to bytes
def makeBytes(num_decks: int) -> list:
    random_seed = 0 # Base value, increased with each batch of decks
    loop_data = []
    convert_data = []
    write_data = []

    zeros = np.zeros(shape=HALF_DECK, dtype='u1')
    ones = np.ones(shape=HALF_DECK, dtype='u1')
    orig_deck = np.concatenate((zeros, ones))

    num_files = int(np.ceil(num_decks/NUM_DECKS_FILE)) # Calculate how many files we will need,
    # handles cases when 15000 decks are requested, etc.

    for _ in range(num_files):
        decks = []
        random_seed+=1
        np.random.seed(random_seed) # Set random seed for shuffling this batch of decks

        t0 = time.time() 
        # Measure how long this loop takes to run
        for __ in range(NUM_DECKS_FILE):
            temp_deck = orig_deck.copy()
            np.random.shuffle(temp_deck)
            decks.append(temp_deck)

        t1 = time.time()
        loop_data.append(t1-t0)

        t2 = time.time()
        # Measure how long it takes to convert data to bytes
        decks_bytes = np.array(decks).tobytes()
        t3 = time.time()

        convert_data.append(t3-t2)

        name = f'bytes_{random_seed}_{len(decks)}.bin'
        path = os.path.join('testing', 'data', 'bindata', name)
        t4 = time.time()
        # Measure how long it takes to write data to file
        with open(path, "wb") as file:
            file.write(decks_bytes)
        t5 = time.time()
        
        write_data.append(t5-t4)

    # return time data
    return [loop_data, write_data, convert_data]
import os
import numpy as np

def getRandomSeed(path_to_data: str) -> int:
    # Read data dir, if empty return 0
    # if not empty return the seed of the last file generated
    # ...or just start random_seed at zero and return the number of files in the directory
    files = os.listdir(path_to_data)
    return len(files)

def makeDecks(half_deck: int, num_decks: int, num_decks_file: int, path_to_data: str) -> None:

    if num_decks < num_decks_file: # num_decks_file should not be greater than the number of decks to write
        num_decks_file = num_decks

    random_seed = getRandomSeed(path_to_data) # Base value, increased with each batch of decks

    zeros = np.zeros(shape=half_deck, dtype='u1')
    ones = np.ones(shape=half_deck, dtype='u1')
    orig_deck = np.concatenate((zeros, ones))

    num_files = int(np.ceil(num_decks/num_decks_file)) # Calculate how many files we will need,
    # handles cases when 15000 decks are requested, etc.

    for _ in range(num_files):
        decks = []
        random_seed+=1
        np.random.seed(random_seed) # Set random seed for shuffling this batch of decks

        for __ in range(num_decks_file):
            temp_deck = orig_deck.copy()
            np.random.shuffle(temp_deck)
            decks.append(temp_deck)

        decks_bytes = np.array(decks).tobytes()

        name = f'bytes_{random_seed}_{len(decks)}.bin'
        path = os.path.join(path_to_data, name)

        with open(path, "wb") as file:
            file.write(decks_bytes)
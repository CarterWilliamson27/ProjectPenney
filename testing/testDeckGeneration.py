import numpy as np
import os

# Method 1: np.array with u1 (this is what Ron does)
HALF_DECK = 26
RANDOM_SEED = 12
zeros = np.zeros(shape=HALF_DECK, dtype='u1')
ones = np.ones(shape=HALF_DECK, dtype='u1')
deck = np.concatenate((zeros, ones))

np.random.seed(RANDOM_SEED)
np.random.shuffle(deck)
print(deck)

# Method 2: np.array.tobytes()
data = deck.tobytes()
full_filename = os.path.join('data', 'tempbytes.txt')
#with open(full_filename, 'wb') as file:
#    file.write(data)

with open(full_filename, 'rb') as file:
    bdata = file.read()
print(bdata)

numpy_array = np.frombuffer(bdata, dtype='u1')

print(numpy_array)
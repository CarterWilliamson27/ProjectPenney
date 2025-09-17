import os
from testing.src.generateDecks import makeDecks, makeBytes
from testing.src.readDecks import test_read_data

# Run tests for .npy and .bin files
# Run given number of iterations of a give number of decks each
# Clear data directories on each iteration

# Helper method to clean out the data directory on each iteration
def clear_dir(path: str) -> None:
    files = os.listdir(os.path.join('testing', 'data', path))
    for file in files:
        os.remove(os.path.join('testing', 'data', path, file))

# Run tests and return results for .npy files
def runNpyTests(num_iterations: int, num_decks: int) -> list:
    npy_data = [['iteration', 'generation_time', 'write_time', 'read_time']]

    for i in range(num_iterations):
        print(f'iteration: {i}')
        # Clear files out of data dir
        clear_dir('npydata')

        generation_time, write_time = makeDecks(num_decks)
        read_time = test_read_data(isBinData=False)

        npy_data.append([generation_time, write_time, read_time])

    return npy_data

# Run tests for .bin
def runBinTests(num_iterations: int, num_decks: int) -> list:
    bin_data = [['iteration', 'generation_time', 'write_time', 'conversion_time', 'read_time']]

    for i in range(num_iterations):
        print(f'iteration: {i}')
        # Clear files out of data dir
        clear_dir('bindata')

        generation_time, write_time, convert_time = makeBytes(num_decks)
        read_time = test_read_data(isBinData=True)

        bin_data.append([generation_time, write_time, convert_time, read_time])

    return bin_data









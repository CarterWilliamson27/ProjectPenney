from testing.src.performanceTests import runNpyTests, runBinTests
from testing.src.compileData import npyCompileData, binCompileData
from testing.src.buildMarkdownFile import buildMarkdownFile
import time

# Run tests for .npy and .bin files
# Run 10 iterations of 2 million decks each, save stats on results
# Should take about 30 minutes to run all tests

NUM_ITERATIONS = 10
NUM_DECKS = 2000000

# .npy files
print(f"running .npy tests ({NUM_ITERATIONS} iterations, {NUM_DECKS} decks per iteration)")

t0 = time.time()
npy_data = runNpyTests(NUM_ITERATIONS, NUM_DECKS)
t1 = time.time()

print("compiling npy data")
npyCompileData(npy_data)
t2 = time.time()

# .bin files
print(f"running .bin tests ({NUM_ITERATIONS} iterations, {NUM_DECKS} decks per iteration)")

t3 = time.time()
bin_data = runBinTests(NUM_ITERATIONS, NUM_DECKS)
t4 = time.time()
print("compiling bin data")
binCompileData(bin_data)
t5 = time.time()

print("done!")
print(f"Meta-stats for {NUM_ITERATIONS} iterations of tests, {NUM_DECKS} decks per iteration: ")
print(f"Total time for program to complete: {t5-t0:.2f} seconds")
print(f"Time to run npy tests: {t1-t0:.2f} seconds")
print(f"Time to compile npy data: {t2-t1:.5f} seconds")
print(f"Time to run bin tests: {t4-t3:.2f} seconds")
print(f"Time to compile bin data: {t5-t4:.5f} seconds")

print('generating markdown file...')
buildMarkdownFile(NUM_ITERATIONS, NUM_DECKS)
print('done!')






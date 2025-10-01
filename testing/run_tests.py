from testing.src.performanceTests import runNpyTests, runBinTests
from testing.src.compileData import npyCompileData, binCompileData
from testing.src.buildMarkdownFile import buildMarkdownFile
import time
import os
import sys

terminaloutput = [] # save inputs and outputs from this script to a file
def mylog(string: str) -> None:
    terminaloutput.append(string)
    print(string)

def myinput(string: str) -> str:
    answer = input(string)
    terminaloutput.append(string+answer)
    return answer

def getUserInput() -> list:
    num_iterations = 10 # default
    num_decks = 2000000 # default
    mylog(f"Hello! You can view the writeup, script log, and data outputs from the default parameters ({num_iterations} iterations, {num_decks} decks per iteration) at " \
          "testing/outputs/default.\nThe tests with the default parameters take about 3 minutes on a 13th Gen Intel i7 CPU with 16GB of RAM, so they may take longer depending on how beefy your setup is." \
            "\n(Please be nice, I did not write strong input validation)")
    answer = myinput("Would you like to run tests with custom parameters (y) or rerun the default tests (n)? (y/n): ")
    if answer == 'n':
        return num_iterations, num_decks
    if answer == 'y':
        confirm = 'n'
        while confirm != 'y':
            input = myinput("How many iterations would you like to run?: ")
            num_iterations = int(input)
            input = myinput("How many decks should be generated per iteration, in units of hundred thousand? (5 = 500k, 10 = 1 million): ")
            num_decks = int(input) * 100000
            confirm = myinput(f"You are about to run {num_iterations} tests with {num_decks} decks per iteration. Proceed (y) or reinput parameters (n): ")
        return num_iterations, num_decks
    else:
        sys.exit("I asked you to be nice with the input...")

# Run tests for .npy and .bin files
# Run 10 iterations of 2 million decks each, save stats on results
# Should take about 6 minutes to run all tests

NUM_ITERATIONS, NUM_DECKS = getUserInput()


# .npy files
mylog(f"running tests for Method 1 ({NUM_ITERATIONS} iterations, {NUM_DECKS} decks per iteration)")

t0 = time.time()
npy_data = runNpyTests(NUM_ITERATIONS, NUM_DECKS)
t1 = time.time()

mylog("compiling Method 1 data")
npyCompileData(npy_data)
t2 = time.time()

# .bin files
mylog(f"running tests for Method 2 ({NUM_ITERATIONS} iterations, {NUM_DECKS} decks per iteration)")

t3 = time.time()
bin_data = runBinTests(NUM_ITERATIONS, NUM_DECKS)
t4 = time.time()
mylog("compiling Method 2 data")
binCompileData(bin_data)
t5 = time.time()

mylog("done!")
mylog(f"Meta-stats for {NUM_ITERATIONS} iterations of tests, {NUM_DECKS} decks per iteration: ")
mylog(f"Total time for program to complete: {t5-t0:.2f} seconds")
mylog(f"Time to run Method 1 tests: {t1-t0:.2f} seconds")
mylog(f"Time to compile Method 1 data: {t2-t1:.5f} seconds")
mylog(f"Time to run Method 2 tests: {t4-t3:.2f} seconds")
mylog(f"Time to compile Method 2 data: {t5-t4:.5f} seconds")

mylog('generating markdown file...')
buildMarkdownFile(NUM_ITERATIONS, NUM_DECKS)
mylog('done! You can find the summary and script log at /testing/outputs!')

# Save this script's output to file
with open(os.path.join("testing", "outputs", "run_tests_log.txt"), "w") as file:
    for line in terminaloutput:
        file.write(line+"\n")







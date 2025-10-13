import os
from src.deckGeneration import makeDecks
from src.scoring import score_files
from src.compileResult import compileResults
from src.generateHeatmap import generateHeatmaps
import time

HALF_DECK = 26
NUM_DECKS_FILE = 10000
PATH_TO_DATA = os.path.join('data')
PATH_TO_SCORES = os.path.join('outputs', 'scores.csv')
PATH_TO_OUTPUT = os.path.join('outputs', 'output.csv')
PATH_TO_HEATMAPS = os.path.join('outputs')

def getUserInput() -> int:
    response = input("Hello! You can find the generated heatmaps under the outputs folder.\n" \
    "How many decks would you like to generate and score? (0 to quit): ")
    num_decks = int(response)
    if num_decks != 0:
        response = input(f"You are about to generate and score {num_decks:,} decks. Proceed? (y/n): ")
        if response.lower() == 'y':
            return num_decks
    
    exit(0)

def augment_data(n: int) -> None:
    # Uncomment lines to run functions

    print("generating decks...")
    # Generate decks
    makeDecks(half_deck=HALF_DECK, num_decks=n, num_decks_file=NUM_DECKS_FILE, path_to_data=PATH_TO_DATA)

    t1 = time.time()
    print("scoring...")
    # Score each deck, change filename to scored, update scores csv with scores
    score_files(path_to_data=PATH_TO_DATA, path_to_scores=PATH_TO_SCORES)
    t2 = time.time()

    print("compiling results...")
    # Compile data into something readable
    compileResults(path_to_scores=PATH_TO_SCORES, path_to_output=PATH_TO_OUTPUT)

    print("generating heatmaps...")
    # generate heatmap of results
    generateHeatmaps(path_to_data=PATH_TO_OUTPUT, path_to_heatmaps=PATH_TO_HEATMAPS)

    print(f"Total time to score {n:,} decks: {t2-t1:.2f} seconds")

if __name__ == "__main__":
    n = getUserInput()
    augment_data(n)



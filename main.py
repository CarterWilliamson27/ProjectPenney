import os
from src.deckGeneration import makeDecks
from src.scoring import score_files
from src.compileResults import compileResults

HALF_DECK = 26
NUM_DECKS_FILE = 10000
NUM_DECKS_TOTAL = 1000000
PATH_TO_DATA = os.path.join('data')
PATH_TO_SCORES = os.path.join('outputs', 'scores.csv')
PATH_TO_OUTPUT = os.path.join('outputs', 'output.csv')

print("generating decks...")
# Generate decks
makeDecks(half_deck=HALF_DECK, num_decks=NUM_DECKS_TOTAL, num_decks_file=NUM_DECKS_FILE, path_to_data=PATH_TO_DATA)

print("scoring...")
# Score each deck, change filename to scored, update scores csv with scores
score_files(path_to_data=PATH_TO_DATA, path_to_scores=PATH_TO_SCORES)

print("compiling results...")
# Compile data into something readable
compileResults(path_to_scores=PATH_TO_SCORES, path_to_output=PATH_TO_OUTPUT)



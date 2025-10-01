import numpy as np
import os
import csv

def compileResults(path_to_scores: str, path_to_output: str) -> None:
    # Read in scored deck data from the file at path_to_scores
    # output human-readable csv to path_to_output

    # example header: p1_choice, p2_choice, trick_ties, p1_trick_wins, p1_trick_loss, card_ties, p1_card_wins, p1_card_loss
    # example input: 000,001,154065,403729,442206,19913,471668,508419,


    # expected output written to csv (obviously our percents will be more accurate in the final product, but for now we just need to show something): 
    # header: p1_choice, p2_choice, p1_win%_tricks, tricks_tie%, p1_win%_cards, cards_tie%
    # data:   RRR        RRB               40.3         15.4           47.2         2.0 

    # we can encode 0 as R and 1 as B (or the other way around, as long as it's consistent)

    pass
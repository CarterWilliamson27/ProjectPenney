import os
import numpy as np
import csv

def score_files(path_to_data: str, path_to_scores: str) -> None:
    # For each file in path_to_data, score each deck in the file against the 56 possible games
    # Then write scores into path_to_scores dir
    # Each deck has 56 rows, for each combination of 8 x 8 possible games - games where the choices are equal
    # variables = p1_choice, p2_choice, p1_cards, p2_cards, p1_tricks, p2_tricks
    
    POSSIBLE_CHOICES = ["000", "001", "010", "011", "100", "101", "110", "111"]
    FIELD_NAMES = ["trick_ties", "p1_trick_wins", "p1_trick_loss", "card_ties", "p1_card_wins", "p1_card_loss"]
    scores = {} # Holds all scores
    #init scores dict, set everything to 0
    for p1_choice in POSSIBLE_CHOICES:
        scores[p1_choice] = {}
        for p2_choice in POSSIBLE_CHOICES:
            if p1_choice == p2_choice: # Skip games where choices are the same
                continue

            scores[p1_choice][p2_choice] = {}
            for field in FIELD_NAMES:
                scores[p1_choice][p2_choice][field] = 0

    unscored_files = os.listdir(path_to_data)
    for file_name in unscored_files:
        if file_name[0] == "s": # scored deck
            continue
        results_list = [] # Clear this list every file to avoid it from growing too large in memory
        file_path = os.path.join(path_to_data, file_name)
        with open(file_path, 'rb') as file:
            deck = file.read(52)
            while deck: # while we have something from the last read
                for p1_choice in POSSIBLE_CHOICES:
                    for p2_choice in POSSIBLE_CHOICES:
                        if p1_choice == p2_choice: # Skip games where choices are the same
                            continue
                        else:
                            p1_tricks, p1_cards, p2_tricks, p2_cards = score_deck(deck, p1_choice, p2_choice)
                            results_list.append([p1_choice, p2_choice, p1_tricks, p1_cards, p2_tricks, p2_cards])
                deck = file.read(52) # Get next deck
        
        # update the overall scores with scores from this file
        scores = update_scores(results_list, scores)
        # Once we are done scoring, rename the file to indicate that it has been scored
        os.rename(file_path, os.path.join(path_to_data, "scored_"+file_name))

    # combine scores from these new files with old scores
    scores = read_previous_scores(path_to_scores=path_to_scores, data_dict=scores)

    # Save scores to csv
    save_scores(path_to_scores, scores)
                        
                
def score_deck(deck: bytes, p1_choice: str, p2_choice: str) -> tuple[int, int, int, int]:
    running_tally = p1_tricks = p1_cards = p2_tricks = p2_cards = 0
    card_0 = None
    card_1 = None
    for card_2 in deck:
        running_tally += 1

        if card_0 is None:
            card_0 = card_2
            continue

        if card_1 is None:
            card_1 = card_2
            continue

        selection = f'{card_0}{card_1}{card_2}'
        if selection == p1_choice:
            p1_tricks+=1
            p1_cards+=running_tally
            running_tally=0
            card_0 = None
            card_1 = None
            continue

        if selection == p2_choice:
            p2_tricks+=1
            p2_cards+=running_tally
            running_tally=0
            card_0 = None
            card_1 = None
            continue
        
        card_0 = card_1
        card_1 = card_2
    
    return p1_tricks, p1_cards, p2_tricks, p2_cards

def read_previous_scores(path_to_scores: str, data_dict: dict) -> dict:
    if not os.path.exists(path_to_scores): # first time scoring ever
        return data_dict
    

    with open(path_to_scores, 'r') as file:
        csv_reader = csv.reader(file, skipinitialspace=True)

         # Header row
        field_names = next(csv_reader)

        for row in csv_reader:
            for i in range(2, len(row)): # skip the p1 and p2 choices, we manually access them
                p1_choice = row[0]
                p2_choice = row[1]
                data_dict[p1_choice][p2_choice][field_names[i]] += int(row[i])


    return data_dict

def update_scores(results: list, scores_dict: dict) -> dict:
    # example result: [p1_choice: 000, p2_choice: 001, p1_tricks: 5, p1_cards: 29, p2_tricks: 2, p2_cards: 21]
    # output: dictionary[p1_choice][p2_choice][wins_tricks|loses_tricks|ties_tricks|wins_cards|loses_cards|ties_cards]
    for result in results:
        # name result fields for code readability
        p1_choice = result[0]
        p2_choice = result[1]
        p1_tricks = result[2]
        p1_cards = result[3]
        p2_tricks = result[4]
        p2_cards = result[5]
        p1_trick_win = p1_tricks > p2_tricks
        trick_tie = p1_tricks == p2_tricks
        p1_card_win = p1_cards > p2_cards
        card_tie = p1_cards == p2_cards
        if trick_tie:
            scores_dict[p1_choice][p2_choice]["trick_ties"] += 1
        elif p1_trick_win:
            scores_dict[p1_choice][p2_choice]["p1_trick_wins"] += 1
        else:
            scores_dict[p1_choice][p2_choice]["p1_trick_loss"] += 1
        
        if card_tie:
            scores_dict[p1_choice][p2_choice]["card_ties"] += 1
        elif p1_card_win:
            scores_dict[p1_choice][p2_choice]["p1_card_wins"] += 1
        else:
            scores_dict[p1_choice][p2_choice]["p1_card_loss"] += 1
    return scores_dict


def save_scores(path: str, scores: dict) -> None:
    extracted_field_names = [item for item in scores['000']['001']] # In case we change order/names, just use what the dictionary has
    field_names = "p1_choice, p2_choice, "+ ", ".join(extracted_field_names)
    formatted_scores = ""
    for p1_choice in scores:
        for p2_choice in scores[p1_choice]:
            formatted_scores += p1_choice + "," + p2_choice + ","
            for item in scores[p1_choice][p2_choice]:
                formatted_scores += str(scores[p1_choice][p2_choice][item]) + ","

            # chop off last comma 
            formatted_scores = formatted_scores[:-1]  
            # add newline  
            formatted_scores += "\n"
            
    with open(os.path.join(path), "w") as file:
        file.write(field_names + "\n")
        file.write(formatted_scores)




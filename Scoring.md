## Project Penney Scoring<br><sup>Carter Williamson & Ruihan Fang</sup>

The scoring method chosen is to keep track of the current three cards in play, and check each player's sequence against these three cards. First, there are counters initialized for each player's won tricks and won cards. There also exists a counter to track how many cards have been drawn for the trick. If neither player's sequence matches the current three cards, a new card replaces the third card in the sequence, the old third card replaces the second, and the old second replaces the first.  Once a player sequence matches the current cards in play, the number of cards drawn is added to the player’s counter of cards won, and that player’s tricks won counter is incremented. The counter for the number of cards drawn is reset, then three new cards are drawn to start the next trick.

Example: 

Setup:

Deck = R, B, R, R, B, B, …

Player 1’s choice: RRR, tricks won = 0, cards won = 0

Player 2’s choice: RRB, tricks won = 0, cards won = 0

card 1, card 2, and card 3 start out as nothing

Number of cards drawn = 0

Gameplay:

Deck: B, R, R, B, B, …

Card 1: none

Card 2: none

Card 3: R

Number of cards drawn = 1

No comparisons done as not all cards have values

Continue to next card
___

Deck: R, R, B, B, …

Card 1: none

Card 2: R

Card 3: B

Number of cards drawn = 2

No comparisons done as not all cards have values

Continue to next card
___

Deck: R, B, B, …

Card 1: R

Card 2: B

Card 3: R

Number of cards drawn = 3

Current sequence in play: RBR

Comparison against player 1’s sequence: RBR != RRR

Comparison against player 2’s sequence: RBR != RRB

Continue to next card
___

Deck: B, B …

Card 1: B

Card 2: R

Card 3: R

Number of cards drawn = 4

Current sequence in play: BRR

Comparison against player 1’s sequence: BRR != RRR

Comparison against player 2’s sequence: BRR != RRB

Continue to next card
___

Deck: B, …

Card 1: R

Card 2: R

Card 3: B

Number of cards drawn = 5

Current sequence in play: RRB

Comparison against player 1’s sequence: BRR != RRR

Comparison against player 2’s sequence: BRR == RRB

Player 2 won!

Player 2 tricks 0 -> 1

Player 2 cards won 0 -> 5

Number of cards drawn 5 -> 0

Reset card 1, card 2, card 3

Continue to next card
___


Deck: …

Card 1: none

Card 2: none

Card 3: B

Number of cards drawn = 1

No comparisons done as not all cards have values

Continue to next card

End of example
___


After the deck is exhausted of cards, the data from the game (player’s choices, number of tricks won, number of cards won) are added to a list of all game results from the decks in the file that we are reading out of. 

After all the decks in a file have been played, the list of results is converted into a dictionary of outcomes (being that Player 1 won, lost, or tied that specific game), indexed by Player 1 and Player 2’s chosen sequences for a fast lookup. This dictionary is cumulative for all of the files that are currently being scored by the program. 

Once all the files have been scored, the dictionary of outcomes is combined with the existing data (from previous executions of the program) in scores.csv. 

___

For things we tried: 

Originally we were going to store the results of each individual game from each individual deck into a file, but that proved to be too much data to work with, both from a runtime and storage perspective. 

There was also an idea to compare the first card in play to the first card in each player's sequence, and if a match is found in either player's sequence, then the second card in play is compared to the second card in whichever sequence (or both) that had a match, and then the same for the third card in play. This implementation looked very clunky, with several nested if statements, and the optimization in runtime was negligible. If we were comparing player sequences of a much larger number of cards, then short-circuiting the comparison would be more optimal, but since there's only three cards to be compared, combining them and comparing the whole combination to the players' choices is not a major optimization issue.  

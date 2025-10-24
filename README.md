# Overview

This project simulates the results of Penney's Game and its variants by generating simple representations of a standard deck of 52 playing cards, playing games with every possible combination of choices that the players can make, and tallying the results.

## Penney's Game
Penney's Game is a two-player sequence-choosing game in which Player 1 chooses a sequence of 3 coin flip results (heads or tails), such as tails, heads, tails, and then Player 2, with knowledge of Player 1's choice, chooses their own sequence of 3 coin flip results, such as tails, tails, heads. A coin is then flipped until one of the player's sequences comes up, and they are declared the winner. [Wikipedia](https://en.wikipedia.org/wiki/Penney%27s_game)
## Humble-Nishiyama Game
A variant to Penney's Game is the Humble-Nishiyama Game, in which a standard deck of 52 playing cards is used instead of a coin. The player's sequences are then in terms of either red cards or black cards, instead of heads or tails. An example sequence would be red card, black card, red card. Cards are revealed from the deck one at a time until one of the player's sequences comes up. That player wins a "trick" and all the revealed cards are removed from play. This continues until all the cards in the deck have been revealed, then the player with the most tricks won is declared the winner.
## Ron's Variant
Ron's Variant to the Humble-Nishiyama Game is to instead of a trick being awarded when a player's sequence comes up, they instead take all the cards that have been revealed and add them to their pile. When all the cards in the deck have been revealed, the player with the most cards in their pile wins.

## Strategy
All three games are non-transitive, meaning that for Player 1's chosen sequence, there is always a sequence for Player 2 to choose that has a higher probability of winning. This project's purpose is to determine the best sequence for Player 2 given the sequence that Player 1 chose, examining winning sequences by tricks (Humble-Nishiyama Game) and by cards (Ron's Variant). When playing by tricks, a simple, closed form solution to winning exists - that being for a Player 1's sequence 123, Player 2's higher-winning sequence is always in the form of 
$$\neg2 1 2$$
 For example, if Player 1 chooses a sequence of Red, Black, Black, Player 2 would choose a sequence of Red, Red, Black, with about an 88% winrate. <br>When playing by cards, this same solution exists, for the most part. What's interesting is that when Player 1 chooses an alternating sequence, that being Red, Black, Red or Black, Red, Black, the highest winning sequence for Player 2 for cards is the inverse of what it is for tricks. It remains unknown why this phenomenon occurs.

# Quickstart

All results and data for this project are found in the outputs folder. scores.csv has the raw data, output.csv has the data represented as a win-rate percentage, and ByCards.svg and ByTricks.svg are heatmap visualizations that show the win-rate of Player 2's choice (x-axis) given Player 1's choice (y-axis).

If you wish to do your own simulations, follow these instructions:

You will need the uv module installed to run this project.
https://github.com/astral-sh/uv

After installing uv, navigate to the root directory of this project, and type the following into the terminal:

```uv sync```

This will set up the virtual environment on your local machine to run the code. Then type:

```uv run main.py```

This will prompt you for a number of decks, and then generate and score that number of decks. Currently there are 5 million decks in use, any additional decks generated will be added to this total.

To start this project fresh, you can clear out the data and outputs directory, and then run main.py.





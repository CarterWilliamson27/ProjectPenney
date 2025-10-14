import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

def retrieve_data(path_to_data: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    data = pd.read_csv(path_to_data)
    trick_data = data[['p1_choice', 'p2_choice', 'p1_win%_tricks','tricks_tie%', 'games_total']]
    card_data = data[['p1_choice', 'p2_choice', 'p1_win%_cards','cards_tie%', 'games_total']]
    return trick_data, card_data

def format_data(title: str, data: pd.DataFrame) -> pd.DataFrame:
    # Input: Full data, with the title either tricks or cards
    # Output: only the data related to the given title
    title = title.lower()
    refined_data = data[['p1_choice', 'p2_choice', 'games_total']]
    winperc = data[f"p1_win%_{title}"].apply(lambda x: str(int((round(float(x[:-1]), 0))))) # round value
    tieperc = data[f"{title}_tie%"].apply(lambda x: "("+str(int((round(float(x[:-1]), 0))))+")") # Add () around rounded value 
    refined_data.insert(loc=0, column="winperc", value=winperc.astype(float))
    refined_data.insert(loc=0, column="win_tie_perc", value=winperc+tieperc)
    return refined_data

def build_heatmap(title: str, data: pd.DataFrame, save_path: str) -> None:
    data = format_data(title, data) # One could argue if this should be called before calling build_heatmap
    games_total = data["games_total"][0]

    # Begin charting
    plt.figure(figsize = [8, 8])
    
    ax = sns.heatmap(data=data.pivot(index="p2_choice", columns="p1_choice", values="winperc"), 
                annot=data.pivot(index="p2_choice", columns="p1_choice", values="win_tie_perc"), fmt="s",
                cmap="Blues", cbar=False, linewidths=0.5)
    plt.title(f"My Chance of Win(Draw)\nBy {title}\nN={games_total:,}", pad=10)
    plt.xlabel("My Choice")
    plt.ylabel("Opponent Choice")
    plt.yticks(rotation=0)

    # Begin box drawing

    # First draw gray boxes over the diagonal
    # Then draw boxes around each "best choice"
    # for each choice, find max value location and add a border to it
    unique_choice = data['p2_choice'].unique()
    unique_choice.sort()
    for i in range(len(unique_choice)):

        # Make diagonals gray
        ax.add_patch(plt.Rectangle((i, i), 1, 1, fill=True, facecolor='darkgray', edgecolor='white', lw=0.5))

        # Find which p1_choice has the highest win% for each p2_choice
        best_p1_choice = data.iloc[data[data['p2_choice'] == unique_choice[i]]['winperc'].idxmax()]['p1_choice']
        # Draw border at the location of the best p1_choice for the given p2_choice
        ax.add_patch(plt.Rectangle((np.where(unique_choice == best_p1_choice)[0][0], i), 1, 1, fill=False, edgecolor='black', lw=2))
    
    # save figure
    plt.savefig(os.path.join(save_path, f'By{title}.svg'), bbox_inches = 'tight', facecolor = 'white')

def generateHeatmaps(path_to_data: str, path_to_heatmaps: str) -> None:
    trick_data, card_data = retrieve_data(path_to_data=path_to_data)
    build_heatmap("Tricks", trick_data, path_to_heatmaps)
    build_heatmap("Cards", card_data, path_to_heatmaps)
    
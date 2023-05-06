import pandas as pd
import numpy as np

class DataFrameManager:

    player_df = 0
    game_df = 0
    team_df = 0
    whole_df = 0

    # On init, create dataframes for comboboxes and add IDs to data to improve performance 
    def __init__(self):

        print('Dataframe initializing...')
        raw_data_csv = 'olympic_womens_dataset.csv'
        raw_dataframe = pd.read_csv(raw_data_csv)

        ##### Assigning IDs to all players, games and teams to make comparison easier ######

        # Dataframe of players (w/o their teams)
        player_array = pd.unique(raw_dataframe[['Player', 'Player 2']].values.ravel('K')).tolist()
        player_series = pd.Series(player_array).dropna()
        player_df = player_series.to_frame(name='Player')
        player_df['PlayerID'] = range(1, len(player_df) + 1)

        # Dataframe of games
        game_array = raw_dataframe.groupby(["game_date", "Home Team", "Away Team"]).size().keys()
        game_df = pd.DataFrame(game_array.tolist()).rename(columns={0: "game_date", 1: "Home Team", 2: "Away Team"})
        game_df['GameID'] = range(1, len(game_df) + 1)

        # Dataframe of teams
        team_array = pd.unique(raw_dataframe[['Home Team', 'Away Team']].values.ravel('K')).tolist()
        team_series = pd.Series(team_array)
        team_df = team_series.to_frame(name='Team')
        team_df['TeamID'] = range(1, len(team_df) + 1)

        # Merging IDs into dataframe
        raw_dataframe['Team 2'] = raw_dataframe.apply(assignTeam2, axis=1)

        # Merge game IDs
        whole_df = raw_dataframe.merge(game_df, how="left", on=["game_date", "Home Team", "Away Team"])
        
        # Merge team IDs
        whole_df = whole_df.merge(team_df, how="left", on="Team")
        whole_df = whole_df.merge(team_df, how="left", left_on="Team 2", right_on="Team", suffixes=["","2"])

        # Merge player IDs
        whole_df = whole_df.merge(player_df, how="left", on="Player")
        whole_df = whole_df.merge(player_df, how="left", left_on="Player 2", right_on="Player", suffixes=["","2"])

        # Dropping unnecessary columns
        whole_df = whole_df.drop(columns=["Player2", "Team2"])

        # Adding team IDs to player dataframe to make filtering easier

        # Player 1
        player_team_array = whole_df.groupby(["PlayerID", "TeamID"]).size().keys()
        player_team_df = pd.DataFrame(player_team_array.tolist()).rename(columns={0: "PlayerID", 1: "TeamID"})

        # Player 2
        player_team2_array = whole_df.groupby(["PlayerID2", "TeamID2"]).size().keys()
        player_team2_df = pd.DataFrame(player_team2_array.tolist()).rename(columns={0: "PlayerID", 1: "TeamID"})
        player_team2_df = player_team2_df.astype({"PlayerID":'int', "TeamID":'int'}) 

        # Merge dataframes
        all_player_team_df = player_team_df.merge(player_team2_df, how="outer")
        all_player_team_df = player_df.merge(all_player_team_df, how="left")

        # Assigning dataframes to class properties
        self.game_df = game_df
        self.player_df = all_player_team_df
        self.team_df = team_df
        self.whole_df = whole_df

        print('Data parsing complete.')

# Checks the event Player 2 is involved in and determines which team they are on (by ID)
def assignTeam2(row):
    is_opp_team = False
    if row['Event'] == 'Faceoff Win' or row['Event'] == 'Zone Entry' or row['Event'] == 'Penalty Taken': is_opp_team = True

    if type(row['Player 2']) == str and row['Team'] == row['Away Team'] and is_opp_team == True: return row['Home Team']
    elif type(row['Player 2']) == str and row['Team'] == row['Away Team'] and is_opp_team == False: return row['Away Team']
    elif type(row['Player 2']) == str and row['Team'] == row['Home Team'] and is_opp_team == True: return row['Away Team']
    elif type(row['Player 2']) == str and row['Team'] == row['Home Team'] and is_opp_team == True: return row['Home Team']
    else: return np.NaN


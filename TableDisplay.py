import pandas as pd
import numpy as np

class TableDisplay:

    def __init__(self, df):
        self.df = df

    # Loads table of individual events
    def individual_table(self, game_id, team_id, player_id, events):
        show_shots = 0
        show_goals = 0
        show_plays = 0
        show_takes = 0
        show_recs = 0
        show_zones = 0
        show_faces = 0
        show_pens = 0

        # Event filters
        for i in events:
            if str(i) == 'Shot Attempts':
                show_shots = i.get()
            elif str(i) == 'Goals':
                show_goals = i.get()
            elif str(i) == 'Plays':
                show_plays = i.get()
            elif str(i) == 'Takeaways':
                show_takes = i.get()
            elif str(i) == 'Recoveries':
                show_recs = i.get()
            elif str(i) == 'Zone Entries':
                show_zones = i.get()
            elif str(i) == 'Faceoffs':
                show_faces = i.get()
            elif str(i) == 'Penalties':
                show_pens = i.get()
        
        # Filtering by game, team and/or player
        filtered_df = self.df
        if game_id > 0:
            filtered_df = filtered_df.loc[filtered_df['GameID'] == game_id]
        if team_id > 0:
            filtered_df = filtered_df.loc[(filtered_df['TeamID'] == team_id) | (filtered_df['TeamID2'] == team_id)]
        if player_id > 0:
            filtered_df = filtered_df.loc[(filtered_df['PlayerID'] == player_id) | (filtered_df['PlayerID2'] == player_id)]

        # Filtering based on event
        event_df_dict = {}
        if show_shots > 0:
            event_df_dict["shots"] = filtered_df.loc[(filtered_df['Event'] == 'Shot')]
        if show_goals > 0:
            event_df_dict["goals"] = filtered_df.loc[(filtered_df['Event'] == 'Goal')]
        if show_plays > 0:
            event_df_dict["plays"] = filtered_df.loc[(filtered_df['Event'] == 'Play') | (filtered_df['Event'] == 'Incomplete Play')]
        if show_takes > 0:
            event_df_dict["takes"] = filtered_df.loc[(filtered_df['Event'] == 'Takeaway')]
        if show_recs > 0:
            event_df_dict["recs"] = filtered_df.loc[(filtered_df['Event'] == 'Puck Recovery')]
        if show_zones > 0:
            event_df_dict["zones"] = filtered_df.loc[(filtered_df['Event'] == 'Zone Entry') | (filtered_df['Event'] == 'Dump In/Out')]
        if show_faces > 0:
            event_df_dict["faces"] = filtered_df.loc[(filtered_df['Event'] == 'Faceoff Win')]
        if show_pens > 0:
            event_df_dict["pens"] = filtered_df.loc[(filtered_df['Event'] == 'Penalty Taken')]
    
        if(len(event_df_dict.values())>0):
            filtered_df = pd.concat(event_df_dict.values())

        # Adding event details
        filtered_df['Shot Type'] = np.where((filtered_df['Event'] == 'Shot') | (filtered_df['Event'] == 'Goal'), filtered_df['Detail 1'], np.NaN)
        filtered_df['Shot Destination'] = np.where((filtered_df['Event'] == 'Shot') | (filtered_df['Event'] == 'Goal'), filtered_df['Detail 2'], np.NaN)
        filtered_df['Shot Traffic'] = np.where((filtered_df['Event'] == 'Shot') | (filtered_df['Event'] == 'Goal'), filtered_df['Detail 3'], np.NaN)
        filtered_df['Shot One-Timer'] = np.where((filtered_df['Event'] == 'Shot') | (filtered_df['Event'] == 'Goal'), filtered_df['Detail 4'], np.NaN)
        filtered_df['Play Type'] = np.where((filtered_df['Event'] == 'Play') | (filtered_df['Event'] == 'Incomplete Play'), filtered_df['Detail 1'], np.NaN)
        filtered_df['Play Target'] = np.where((filtered_df['Event'] == 'Play') | (filtered_df['Event'] == 'Incomplete Play'), filtered_df['Player 2'], np.NaN)
        filtered_df['Zone Entry Type'] = np.where((filtered_df['Event'] == 'Zone Entry'), filtered_df['Detail 1'], np.NaN)
        filtered_df['Zone Entry Target'] = np.where((filtered_df['Event'] == 'Zone Entry'), filtered_df['Player 2'], np.NaN)
        filtered_df['Dump In Outcome'] = np.where((filtered_df['Event'] == 'Dump In/Out'), filtered_df['Detail 1'], np.NaN)
        filtered_df['Faceoff Loss'] = np.where((filtered_df['Event'] == 'Faceoff Win'), filtered_df['Player 2'], np.NaN)
        filtered_df['Penalty Type'] = np.where((filtered_df['Event'] == 'Penalty Taken'), filtered_df['Detail 1'], np.NaN)
        filtered_df['Penalty Drawn By'] = np.where((filtered_df['Event'] == 'Penalty Taken'), filtered_df['Player 2'], np.NaN)


        # Columns to include
        included_cols = ['game_date', 'Team', 'Player', 'Event', 'Period', 'Clock']
        if show_shots > 0 or show_goals > 0:
            included_cols.append('Shot Type')
            included_cols.append('Shot Destination')
            included_cols.append('Shot Traffic')
            included_cols.append('Shot One-Timer')
        if show_plays > 0:
            included_cols.append('Play Type')
            included_cols.append('Play Target')
        if show_zones > 0:
            included_cols.append('Zone Entry Type')
            included_cols.append('Zone Entry Target')
            included_cols.append('Dump In Outcome')
        if show_faces > 0:
            included_cols.append('Faceoff Loss')
        if show_pens > 0:
            included_cols.append('Penalty Type')
            included_cols.append('Penalty Drawn By')

        return_df = filtered_df[included_cols]
        return return_df

    # Loads table of aggregated stats
    def aggregate_table(self, game_id, team_id, player_id, events, game_df, team_df, player_df):
        show_shots = 0
        show_goals = 0
        show_plays = 0
        show_takes = 0
        show_recs = 0
        show_zones = 0
        show_faces = 0
        show_pens = 0

        # Event filters
        for i in events:
            if str(i) == 'Shot Attempts':
                show_shots = i.get()
            elif str(i) == 'Goals':
                show_goals = i.get()
            elif str(i) == 'Plays':
                show_plays = i.get()
            elif str(i) == 'Takeaways':
                show_takes = i.get()
            elif str(i) == 'Recoveries':
                show_recs = i.get()
            elif str(i) == 'Zone Entries':
                show_zones = i.get()
            elif str(i) == 'Faceoffs':
                show_faces = i.get()
            elif str(i) == 'Penalties':
                show_pens = i.get()
        
        # Filtering by game, team and/or player
        filtered_df = self.df
        if game_id > 0:
            filtered_df = filtered_df.loc[filtered_df['GameID'] == game_id]
        if team_id > 0:
            filtered_df = filtered_df.loc[(filtered_df['TeamID'] == team_id) | (filtered_df['TeamID2'] == team_id)]
        if player_id > 0:
            filtered_df = filtered_df.loc[(filtered_df['PlayerID'] == player_id) | (filtered_df['PlayerID2'] == player_id)]

        # Determining which players to track
        filtered_player_df = player_df
        if game_id > 0:
            home_str = game_df['Home Team'].where(game_df['GameID'] == game_id).dropna().iloc[0]
            away_str = game_df['Away Team'].where(game_df['GameID'] == game_id).dropna().iloc[0]
            home_id = team_df['TeamID'].where(team_df['Team'] == home_str).dropna().iloc[0]
            away_id = team_df['TeamID'].where(team_df['Team'] == away_str).dropna().iloc[0]
            filtered_player_df = filtered_player_df.loc[(filtered_player_df['TeamID'] == home_id) | (filtered_player_df['TeamID'] == away_id)]
        if team_id > 0:
            filtered_player_df = filtered_player_df.loc[(filtered_player_df['TeamID'] == team_id)]
        if player_id > 0:
            filtered_player_df = filtered_player_df.loc[(filtered_player_df['PlayerID'] == player_id)]
        
        # Function that aggregates all selected stas for a player
        def aggregate_all_events(p_id, df):
            temp_series = pd.Series([p_id])
            returned_df = temp_series.to_frame(name='PlayerID')
            player_event_df = df.loc[(df['PlayerID'] == p_id) | (df['PlayerID2'] == p_id)]
            returned_df['Games Played'] = len(player_event_df.groupby(["game_date", "Home Team", "Away Team"]).size().keys())
            
            if show_shots > 0:
                player_shot_df = player_event_df.loc[(player_event_df['Event'] == 'Shot') | (player_event_df['Event'] == 'Goal')]
                returned_df['Shot Attempts'] = player_shot_df['Event'].count()
                returned_df['Shots On Net'] = player_shot_df.loc[(player_shot_df['Detail 2'] == 'On Net')]['Event'].count()
                returned_df['Shots Missed'] = player_shot_df.loc[(player_shot_df['Detail 2'] == 'Missed')]['Event'].count()
                returned_df['Shots Blocked'] = player_shot_df.loc[(player_shot_df['Detail 2'] == 'Blocked')]['Event'].count()

            if show_goals > 0:
                player_shot_df = player_event_df.loc[(player_event_df['Event'] == 'Shot')]
                player_goal_df = player_event_df.loc[(player_event_df['Event'] == 'Goal')]
                returned_df['Goals'] = player_goal_df['Event'].count()
                returned_df['Shooting %'] = round((100 * returned_df['Goals']).divide(player_shot_df.loc[(player_shot_df['Detail 2'] == 'On Net')]['Event'].count() + returned_df['Goals']) , 2).replace(np.inf, 0)

            if show_plays > 0:
                player_play_df = player_event_df.loc[(player_event_df['Event'] == 'Play') | (player_event_df['Event'] == 'Incomplete Play')]
                returned_df['Play Attempts'] = player_play_df.loc[(player_play_df['PlayerID'] == p_id)]['Event'].count()
                returned_df['Complete Plays'] = player_play_df.loc[(player_play_df['PlayerID'] == p_id) & (player_play_df['Event'] == 'Play')]['Event'].count()
                returned_df['Incomplete Plays'] = player_play_df.loc[(player_play_df['PlayerID'] == p_id) & (player_play_df['Event'] == 'Incomplete Play')]['Event'].count()
                returned_df['Targeted Plays'] = player_play_df.loc[(player_play_df['PlayerID2'] == p_id)]['Event'].count()
                returned_df['Targeted Complete Plays'] = player_play_df.loc[(player_play_df['PlayerID2'] == p_id) & (player_play_df['Event'] == 'Play')]['Event'].count()
                returned_df['Targeted Incomplete Plays'] = player_play_df.loc[(player_play_df['PlayerID2'] == p_id) & (player_play_df['Event'] == 'Incomplete Play')]['Event'].count()

            if show_takes > 0:
                player_take_df = player_event_df.loc[(player_event_df['Event'] == 'Takeaway')]
                returned_df['Takeaways'] = player_take_df['Event'].count()

            if show_recs > 0:
                player_rec_df = player_event_df.loc[(player_event_df['Event'] == 'Puck Recovery')]
                returned_df['Recoveries'] = player_rec_df['Event'].count()

            if show_zones > 0:
                player_zone_df = player_event_df.loc[(player_event_df['Event'] == 'Zone Entry') | (player_event_df['Event'] == 'Dump In/Out')]
                returned_df['Carried Zone Entries'] = player_zone_df.loc[(player_zone_df['PlayerID'] == p_id) & (player_zone_df['Detail 1'] == 'Carried')]['Event'].count()
                returned_df['Dumped Zone Entries'] = player_zone_df.loc[(player_zone_df['PlayerID'] == p_id) & (player_zone_df['Detail 1'] == 'Dumped')]['Event'].count()
                returned_df['Played Zone Entries'] = player_zone_df.loc[(player_zone_df['PlayerID'] == p_id) & (player_zone_df['Detail 1'] == 'Played')]['Event'].count()
                returned_df['Dump Ins/Outs Retained'] = player_zone_df.loc[(player_zone_df['PlayerID'] == p_id) & (player_zone_df['Detail 1'] == 'Retained')]['Event'].count()
                returned_df['Dump Ins/Outs Lost'] = player_zone_df.loc[(player_zone_df['PlayerID'] == p_id) & (player_zone_df['Detail 1'] == 'Lost')]['Event'].count()
                returned_df['Carried Zone Entries Against'] = player_zone_df.loc[(player_zone_df['PlayerID2'] == p_id) & (player_zone_df['Detail 1'] == 'Carried')]['Event'].count()
                returned_df['Dumped Zone Entries Against'] = player_zone_df.loc[(player_zone_df['PlayerID2'] == p_id) & (player_zone_df['Detail 1'] == 'Dumped')]['Event'].count()
                returned_df['Played Zone Entries Against'] = player_zone_df.loc[(player_zone_df['PlayerID2'] == p_id) & (player_zone_df['Detail 1'] == 'Played')]['Event'].count()

            if show_faces > 0:
                player_face_df = player_event_df.loc[(player_event_df['Event'] == 'Faceoff Win')]
                returned_df['Faceoff Wins'] = player_face_df.loc[(player_face_df['PlayerID'] == p_id)]['Event'].count()
                returned_df['Faceoff Losses'] = player_face_df.loc[(player_face_df['PlayerID2'] == p_id)]['Event'].count()
                returned_df['Faceoff %'] = round(((100 * returned_df['Faceoff Wins']).divide(returned_df['Faceoff Losses'] + returned_df['Faceoff Wins'])), 2).replace(np.inf, 0)

            if show_pens > 0:
                player_pens_df = player_event_df.loc[(player_event_df['Event'] == 'Penalty Taken')]
                returned_df['Penalties Taken'] = player_pens_df.loc[(player_pens_df['PlayerID'] == p_id)]['Event'].count()
                returned_df['Penalties Drawn'] = player_pens_df.loc[(player_pens_df['PlayerID2'] == p_id)]['Event'].count()
                
            return returned_df

        # Aggregating all data for players
        agg_stat_df = 0
        for index, row in filtered_player_df.iterrows():
                p_id = row['PlayerID']
                df_to_join = aggregate_all_events(p_id, filtered_df)
                if type(agg_stat_df) == int:
                    agg_stat_df = df_to_join
                else:
                    agg_stat_df = pd.concat([agg_stat_df, df_to_join], ignore_index=True)

        # Merging into player table
        complete_merge_df = filtered_player_df.merge(agg_stat_df, how="inner", on="PlayerID")
        complete_merge_df = complete_merge_df.drop(columns=["PlayerID","TeamID"])

        return complete_merge_df
    
    
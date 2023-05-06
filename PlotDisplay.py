import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from hockey_rink import IIHFRink

class PlotDisplay:

    def __init__(self, df):
        self.df = df

    def plot_data(self, game_id, team_id, player_id, events):
        self.show_shots = 0
        self.show_goals = 0
        self.show_plays = 0
        self.show_takes = 0
        self.show_recs = 0
        self.show_zones = 0
        self.show_faces = 0
        self.show_pens = 0

        # Event filters
        for i in events:
            if str(i) == 'Shot Attempts':
                self.show_shots = i.get()
            elif str(i) == 'Goals':
                self.show_goals = i.get()
            elif str(i) == 'Plays':
                self.show_plays = i.get()
            elif str(i) == 'Takeaways':
                self.show_takes = i.get()
            elif str(i) == 'Recoveries':
                self.show_recs = i.get()
            elif str(i) == 'Zone Entries':
                self.show_zones = i.get()
            elif str(i) == 'Faceoffs':
                self.show_faces = i.get()
            elif str(i) == 'Penalties':
                self.show_pens = i.get()

        # Filtering by game, team and/or player
        filtered_df = self.df
        if game_id > 0:
            filtered_df = filtered_df.loc[filtered_df['GameID'] == game_id]
        if team_id > 0:
            filtered_df = filtered_df.loc[(filtered_df['TeamID'] == team_id)]
        if player_id > 0:
            filtered_df = filtered_df.loc[(filtered_df['PlayerID'] == player_id)]

        # Filtering based on event
        event_df_dict = {}
        if self.show_shots > 0:
            event_df_dict["shots"] = filtered_df.loc[(filtered_df['Event'] == 'Shot')]
        if self.show_goals > 0:
            event_df_dict["goals"] = filtered_df.loc[(filtered_df['Event'] == 'Goal')]
        if self.show_plays > 0:
            event_df_dict["plays"] = filtered_df.loc[(filtered_df['Event'] == 'Play') | (filtered_df['Event'] == 'Incomplete Play')]
        if self.show_takes > 0:
            event_df_dict["takes"] = filtered_df.loc[(filtered_df['Event'] == 'Takeaway')]
        if self.show_recs > 0:
            event_df_dict["recs"] = filtered_df.loc[(filtered_df['Event'] == 'Puck Recovery')]
        if self.show_zones > 0:
            event_df_dict["zones"] = filtered_df.loc[(filtered_df['Event'] == 'Zone Entry') | (filtered_df['Event'] == 'Dump In/Out')]
        if self.show_faces > 0:
            event_df_dict["faces"] = filtered_df.loc[(filtered_df['Event'] == 'Faceoff Win')]
        if self.show_pens > 0:
            event_df_dict["pens"] = filtered_df.loc[(filtered_df['Event'] == 'Penalty Taken')]

        if(len(event_df_dict.values())>0):
            filtered_df = pd.concat(event_df_dict.values())

        # Columns to include
        included_cols = ['Player', 'Event', 'X Coordinate', 'Y Coordinate', 'X Coordinate 2', 'Y Coordinate 2']

        return_df = filtered_df[included_cols]
        return return_df

    # Plot all points on rink
    def pointplot(self, df):

        # Getting rink
        fig, axs = plt.subplots(1, 1, sharey=True, figsize=(12, 6), gridspec_kw={"width_ratios": [1]})
        iihf_rink = IIHFRink(x_shift=100, y_shift=42.5, rotation=0)
        axs = iihf_rink.draw(ax=axs)

        # Filtering which events to show and plotting them
        if self.show_shots > 0:
            shot_df = df.loc[(df['Event']== 'Shot')]
            iihf_rink.scatter(shot_df['X Coordinate'], shot_df['Y Coordinate'], color='#808000', s=10, label="Shot")
        
        if self.show_goals > 0:
            goal_df = df.loc[(df['Event']== 'Goal')]
            iihf_rink.scatter(goal_df['X Coordinate'], goal_df['Y Coordinate'], color='#46f0f0', s=50, label="Goal")
        
        if self.show_plays > 0:
            play_comp_df = df.loc[(df['Event'] == 'Play') | (df['Event'] == 'Incomplete Play')]
            play_inc_df = df.loc[(df['Event'] == 'Incomplete Play')]
            iihf_rink.scatter(play_comp_df['X Coordinate'], play_comp_df['Y Coordinate'], color='#e6194b', s=10, label="Passer (Complete)")
            iihf_rink.scatter(play_comp_df['X Coordinate 2'], play_comp_df['Y Coordinate 2'], color='#ffe119', s=10, label="Receiver (Complete)")
            iihf_rink.scatter(play_inc_df['X Coordinate'], play_inc_df['Y Coordinate'], color='#4363d8', s=10, label="Passer (Incomplete)")
            iihf_rink.scatter(play_inc_df['X Coordinate 2'], play_inc_df['Y Coordinate 2'], color='#f58231', s=10, label="Receiver (Incomplete)")
        
        if self.show_takes > 0:
            take_df = df.loc[(df['Event'] == 'Takeaway')]
            iihf_rink.scatter(take_df['X Coordinate'], take_df['Y Coordinate'], color='#911eb4', s=10, label="Takeaway")
       
        if self.show_recs > 0:
            rec_df = df.loc[(df['Event'] == 'Puck Recovery')]
            iihf_rink.scatter(rec_df['X Coordinate'], rec_df['Y Coordinate'], color='#3cb44b', s=10, label="Recovery")
        
        if self.show_zones > 0:
            zone_df = df.loc[(df['Event'] == 'Zone Entry')]
            dump_df = df.loc[(df['Event'] == 'Dump In/Out')]
            iihf_rink.scatter(zone_df['X Coordinate'], zone_df['Y Coordinate'], color='#f032e6', s=10, label="Zone Entry")
            iihf_rink.scatter(dump_df['X Coordinate'], dump_df['Y Coordinate'], color='#bcf60c', s=10, label="Dump In/Out")

        if self.show_faces > 0:
            face_df = df.loc[(df['Event'] == 'Faceoff Win')]
            iihf_rink.scatter(face_df['X Coordinate'], face_df['Y Coordinate'], color='#fabebe', s=10, label="Faceoff Win")
        
        if self.show_pens > 0:
            pen_df = df.loc[(df['Event'] == 'Penalty Taken')]
            iihf_rink.scatter(pen_df['X Coordinate'], pen_df['Y Coordinate'], color='#008080', s=10, label="Penalty Taken")

        axs.legend(loc='upper center', bbox_to_anchor=(0.5, -0.01),
          fancybox=True, shadow=True, ncol=5)

        return fig, axs


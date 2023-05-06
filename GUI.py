import tkinter as tk
from tkinter import ttk as ttk
from DataFrameManager import *
from TableDisplay import *
from pandastable import Table
from PlotDisplay import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 

class GUI:

    selected_game = 0
    selected_team = 0
    selected_player = 0
    event_array = []

    
    def __init__(self, root, data_frame_manager: DataFrameManager):
        print('GUI Initialized')

        # General dataframe
        self.dfm = data_frame_manager

        # Window Canvas
        self.canvas = tk.Canvas(root, width=1250, height=600)
        self.canvas.pack()

        # Creating left and right frames
        self.frm_left = tk.Frame(root, bg='gray92')
        self.frm_left.place(relheight=1, relwidth=0.25)              # Left Frame

        self.frm_right = tk.Frame(root, bg='white')
        self.frm_right.place(relx=0.25, relheight=1, relwidth=0.75)  # Right Frame

         ##### Left frame widgets #####
         
         # Display selection
        self.lbl_display = tk.Label(self.frm_left, text='Display:', bg='gray')
        self.lbl_display.pack(fill='x')
        self.combo_display = ttk.Combobox(self.frm_left, values=['Table - Individual Events', 'Table - Aggregate Events', 'Point Map'])
        self.combo_display.pack(fill='x')
        self.combo_display.current(0)

        self.combo_list_games = []
        self.combo_list_teams = []
        self.combo_list_players = []

        # Creating combobox list of games, Replacing Olympic text because it's ugly
        self.game_array = data_frame_manager.game_df.values.tolist()
        self.combo_list_games.append("All")
        for i in self.game_array:
            home = i[1].replace("Olympic (Women) - ","")
            away = i[2].replace("Olympic (Women) - ","")
            txt = i[0]+ ": " + away + " @ " + home
            self.combo_list_games.append(txt)
        
        self.team_array = []
        self.player_array = []

        # Filter Players based on combobox results
        def filter_players():
            self.combo_list_players = []
            self.combo_list_players.append("All")
            if self.selected_team != 0:
                self.player_array = data_frame_manager.player_df.sort_values('Player').where((data_frame_manager.player_df['TeamID'] == self.selected_team)).dropna().astype({"TeamID":'int', "PlayerID":'int'}).values.tolist()
                for i in self.player_array:
                    self.combo_list_players.append(i[0])
            else: 
                self.player_array = data_frame_manager.player_df.sort_values('Player').values.tolist()
                for i in self.player_array:
                    self.combo_list_players.append(i[0])
            self.combo_player.configure(values=self.combo_list_players)

        # Filter teams based on combobox results
        def filter_teams():
            self.combo_list_teams = []
            self.combo_list_teams.append("All")
            if self.selected_game != 0:
                home_str = data_frame_manager.game_df['Home Team'].where(data_frame_manager.game_df['GameID'] == self.selected_game).dropna().iloc[0]
                away_str = data_frame_manager.game_df['Away Team'].where(data_frame_manager.game_df['GameID'] == self.selected_game).dropna().iloc[0]
                self.team_array = data_frame_manager.team_df.where((data_frame_manager.team_df['Team'] == home_str) | (data_frame_manager.team_df['Team'] == away_str)).dropna().astype({"TeamID":'int'}).values.tolist()
                for i in self.team_array:
                    self.combo_list_teams.append(i[0])
            else: 
                self.team_array = data_frame_manager.team_df.values.tolist()
                for i in self.team_array:
                    self.combo_list_teams.append(i[0])
            self.combo_team.configure(values=self.combo_list_teams)
            filter_players()

        # Game selection
        def pick_game(e):
            game = self.combo_game.get()
            idx = -1
            for i in self.combo_list_games:
                if i == game:
                    break
                idx += 1
            if idx == -1:
                self.selected_game = 0
            else:
                self.selected_game = self.game_array[idx][3]
            self.selected_team = 0
            self.selected_player = 0
            filter_teams()
                
        self.lbl_game = tk.Label(self.frm_left, text='Game:', bg='gray')
        self.lbl_game.pack(fill='x')
        self.combo_game = ttk.Combobox(self.frm_left, values=self.combo_list_games)
        self.combo_game.pack(fill='x')
        self.combo_game.bind("<<ComboboxSelected>>", pick_game)
        self.combo_game.current = 0

        # Team selection
        def pick_team(e):
            team = self.combo_team.get()
            idx = -1
            for i in self.combo_list_teams:
                if i == team:
                    break
                idx += 1
            if idx == -1:
                self.selected_team = 0
            else:
                self.selected_team = self.team_array[idx][1]
            
            self.selected_player = 0
            filter_players()
                
        self.lbl_team = tk.Label(self.frm_left, text='Team:', bg='gray')
        self.lbl_team.pack(fill='x')
        self.combo_team = ttk.Combobox(self.frm_left, values=self.combo_list_teams)
        self.combo_team.pack(fill='x')
        self.combo_team.bind("<<ComboboxSelected>>", pick_team)
        self.combo_team.current = 0

        # Player selection
        def pick_player(e):
            player = self.combo_player.get()
            idx = -1
            for i in self.combo_list_players:
                if i == player:
                    break
                idx += 1
            if idx == -1:
                self.selected_player = 0
            else:
                self.selected_player = self.player_array[idx][1]
             
        self.lbl_player = tk.Label(self.frm_left, text='Player:', bg='gray')
        self.lbl_player.pack(fill='x')
        self.combo_player = ttk.Combobox(self.frm_left, values=self.combo_list_players)
        self.combo_player.pack(fill='x')
        self.combo_player.bind("<<ComboboxSelected>>", pick_player)
        self.combo_player.current = 0
    
        # Event Selection
        self.lbl_events = tk.Label(self.frm_left, text='Events:', bg='gray')
        self.lbl_events.pack(fill='x')
        self.combo_list_events = ['Shot Attempts', 'Goals', 'Plays', 'Takeaways', 'Recoveries', 'Zone Entries', 'Faceoffs', 'Penalties']
        for index, event in enumerate(self.combo_list_events):
            self.event_array.append(tk.IntVar(value=0, name=event))
            tk.Checkbutton(self.frm_left, variable=self.event_array[index], bg='gray92', text=event).pack()
        
        # Show data button
        self.btn_show_data = tk.Button(self.frm_left, text='Show Data', bg='gray92', command=self.show_data)
        self.btn_show_data.pack(fill='x')

    # Chooses which data is to be displayed
    def show_data(self):
        
        ##### Right frame widgets #####

        # Destroying old sub frame and adding a new one in frm_right
        for widget in self.frm_right.winfo_children():
            widget.destroy()
        self.frm_right.pack_forget()
        self.frm_sub = tk.Frame(self.frm_right, bg='white')
        self.frm_sub.place(relx=0, relheight=1, relwidth=1)

        if self.combo_display.get() == 'Table - Individual Events':
            self.individual_table()
        if self.combo_display.get() == 'Table - Aggregate Events':
            self.aggregate_table()
        if self.combo_display.get() == 'Point Map':
            self.point_map()
        
    # Individual events
    def individual_table(self):
        table_display = TableDisplay(self.dfm.whole_df)
        df = table_display.individual_table(self.selected_game, self.selected_team, self.selected_player, self.event_array)
        pt = Table(self.frm_sub, dataframe=df)
        pt.show()

    # Aggregated events
    def aggregate_table(self):
        table_display = TableDisplay(self.dfm.whole_df)
        df = table_display.aggregate_table(self.selected_game, self.selected_team, self.selected_player, self.event_array, self.dfm.game_df, self.dfm.team_df, self.dfm.player_df)
        pt = Table(self.frm_sub, dataframe=df)
        pt.show()
    
    # Map of individual events
    def point_map(self):
        try:
            plot_display = PlotDisplay(self.dfm.whole_df)
            df_plot = plot_display.plot_data(self.selected_game, self.selected_team, self.selected_player, self.event_array)
            fig, axs = plot_display.pointplot(df_plot)

            fig_canvas = FigureCanvasTkAgg(fig, master=self.frm_sub)
            fig_canvas.draw()
            fig_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.Y, expand=1)
        except:
            print('Error on displaying chart')
        
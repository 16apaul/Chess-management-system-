from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from scipy.stats import kendalltau,stats
from models.tournament import Tournament
from models.player import Player
import pandas as pd
import re
class EndTournamentController: # when end tournament is clicked
    
    def __init__(self, main_window):
        self.main_window = main_window
        
    
    def end_tournament(self):
        

        tournament = self.main_window.get_current_tournament()
        players = tournament.players

        # Sort by id
        players_sorted = sorted(players, key=lambda p: p.id, reverse=False)

        self.main_window.results_listbox.clear()
        
        
        
        self.add_to_results_listbox() # outputs players to results listbox sorted by points

        
        y_dict = self.get_actual_dict()

       
        if y_dict is None or len(y_dict) == 0:
            print("No actual results found to compare.")
            return
        # in the dictionaries below x_dict and y_dict will have the ids at the same key indexes. This allows the score to account for ties
        
        x_dict = self.get_sim_dict()
        x_id = list( x_dict.keys())    
        x_score = list(x_dict.values())    
            

        y_dict = self.get_actual_dict()
        y_id =list( y_dict.keys())
        y_score = list(y_dict.values())
        
        #print("simulation ids", x_id)
        #print("sim values", x_score)
        
        #print("actual ids",y_id)
        #print("actual scores,", y_score)
        # calculate kendall tau including ties

        sim_ranks = stats.rankdata([-s for s in x_score], method='average')  # rank the scores
        actual_ranks = stats.rankdata([-s for s in y_score], method='average')
        
      
        tau, p_value = kendalltau(sim_ranks, actual_ranks)
        print("Kendall tau:", tau)
        print("p-value:", p_value)
        self.main_window.submit_results_controller.clear_layout(self.main_window.stats_groupbox_layout)
        
        
        sim_tau_label = QLabel(f"Kendall Tau with ties:{tau}")
        sim_p_label=QLabel(f"P_value{p_value}")
        self.main_window.stats_groupbox_layout.addWidget(sim_tau_label)
        self.main_window.stats_groupbox_layout.addWidget(sim_p_label)
        
        # calculate kendall tau excluding ties

        x_sorted_sim_dict = self.sort_sim_dict()
        x_sorted_ids = list(x_sorted_sim_dict.keys())
        
        y_sorted_actual_dict = self.sort_actual_dict()
        y_sorted_ids = list(y_sorted_actual_dict.keys())
        
        
        tau, p_value = kendalltau(x_sorted_ids, y_sorted_ids) # program forced to rank tied values, ties are broken based on higher id count
        print("Kendall tau:", tau)
        print("p-value:", p_value)        
        
        
        
        
        sim_tau_label = QLabel(f"Kendall Tau with no ties:{tau}")
        sim_p_label = QLabel(f"P_value{p_value}")
        self.main_window.stats_groupbox_layout.addWidget(sim_tau_label)
        self.main_window.stats_groupbox_layout.addWidget(sim_p_label)
        
        
        # get actual and simulated player list in the same order to compare buchholz scores, y_dict and buchholz dict have the same order if ids.
        x_buchholz_dict = self.get_all_buchholz() # buchholz scores for simulated
        x_buchholz = x_buchholz_dict.values()
        x_buchholz_ranked = stats.rankdata([-s for s in x_buchholz], method='average')  # rank the scores
        tau, p_value = kendalltau(x_buchholz_ranked, actual_ranks) # compare buchholz ranking to actual ranking, can compare dur to index of the value of buchollz dict being same as actual dict
        sim_tau_label = QLabel(f"Kendall Tau with buchholz ranking with ties:{tau}") 
        sim_p_label = QLabel(f"P_value{p_value}")
        self.main_window.stats_groupbox_layout.addWidget(sim_tau_label)
        self.main_window.stats_groupbox_layout.addWidget(sim_p_label)
        
        
        
        # sort ranking by the buchholz score then get the rankings of the players based on buchholz score, then get tau and p value
        x_buchholz_dict = self.get_all_buchholz() # buchholz scores for simulated
        x_sorted_buchholz_dict = self.sort_dict_by_value(x_buchholz_dict) # sort by buchholz value
        x_buchholz_ids = list(x_sorted_buchholz_dict.keys()) # get the sorted ids by buchholz
        
        
        tau, p_value = kendalltau(x_buchholz_ids, y_sorted_ids) # compare buchholz ranking to actual ranking
        sim_tau_label = QLabel(f"Kendall Tau with buchholz ranking no ties:{tau}") #
        sim_p_label = QLabel(f"P_value{p_value}")
        self.main_window.stats_groupbox_layout.addWidget(sim_tau_label)
        self.main_window.stats_groupbox_layout.addWidget(sim_p_label)
        
        
        
        # -----------------------
        #  SONNEBORN-BERGER (with ties)
        # -----------------------
        x_sb_dict = self.get_all_sonneborn_berger()
        x_sb_values = x_sb_dict.values()

        # rank scores (higher = better)
        x_sb_ranked = stats.rankdata([-s for s in x_sb_values], method='average')

        tau, p_value = kendalltau(x_sb_ranked, actual_ranks)

        sb_tau_label = QLabel(f"Kendall Tau with SB ranking (ties): {tau}")
        sb_p_label = QLabel(f"P-value: {p_value}")

        self.main_window.stats_groupbox_layout.addWidget(sb_tau_label)
        self.main_window.stats_groupbox_layout.addWidget(sb_p_label)


        # -----------------------
        #  SONNEBORN-BERGER (no ties)
        # -----------------------
        x_sb_sorted = self.sort_dict_by_value(x_sb_dict)
        x_sb_ids = list(x_sb_sorted.keys())

        tau, p_value = kendalltau(x_sb_ids, y_sorted_ids)

        sb_tau_label_no_ties = QLabel(f"Kendall Tau with SB ranking (no ties): {tau}")
        sb_p_label_no_ties = QLabel(f"P-value: {p_value}")

        self.main_window.stats_groupbox_layout.addWidget(sb_tau_label_no_ties)
        self.main_window.stats_groupbox_layout.addWidget(sb_p_label_no_ties)


        # -----------------------
        #  AROC (with ties)
        # -----------------------
        x_aroc_dict = self.get_all_arocs()
        x_aroc_values = x_aroc_dict.values()

        x_aroc_ranked = stats.rankdata([-s for s in x_aroc_values], method='average')

        tau, p_value = kendalltau(x_aroc_ranked, actual_ranks)

        aroc_tau_label = QLabel(f"Kendall Tau with AROC ranking (ties): {tau}")
        aroc_p_label = QLabel(f"P-value: {p_value}")

        self.main_window.stats_groupbox_layout.addWidget(aroc_tau_label)
        self.main_window.stats_groupbox_layout.addWidget(aroc_p_label)


        # -----------------------
        #  AROC (no ties)
        # -----------------------
        x_aroc_sorted = self.sort_dict_by_value(x_aroc_dict)
        x_aroc_ids = list(x_aroc_sorted.keys())

        tau, p_value = kendalltau(x_aroc_ids, y_sorted_ids)

        aroc_tau_label_no_ties = QLabel(f"Kendall Tau with AROC ranking (no ties): {tau}")
        aroc_p_label_no_ties = QLabel(f"P-value: {p_value}")

        self.main_window.stats_groupbox_layout.addWidget(aroc_tau_label_no_ties)
        self.main_window.stats_groupbox_layout.addWidget(aroc_p_label_no_ties)
        
        
        
        
        
        
        
        

        
    def get_actual_dict(self): # gets the actual rankings where key is id and value is points
            tournament= self.main_window.get_current_tournament()
            file = tournament.name
            try:
                # Build the full correct path
                path = file

                # Read the CSV, splitting on tabs
                self.df = pd.read_csv(path, sep="\t", engine="python")
            except Exception as e:
                print("Error loading CSV:", e)
                return

            # clean columns
            self.df.columns = self.df.columns.str.strip()

            #print("Columns:", self.df.columns.tolist())
            players = []
            rankings = {}
            for i, row in self.df.iterrows(): # iterate through each row in the dataframe get id and points and build dictionary
                name = row["Name"]
                rating = row["Rtg"]
                federation = row["FED"]
                points = row["Pts."]
                id = int(row["No."])
                rankings[id] = points
                player = Player(id,name,rating)
                rd_values = []
                for col in self.df.columns:
                    if col.endswith(".Rd"):
                        rd_number = int(col.split(".Rd")[0]) # gets the latest .Rd number
                    
            
                rounds =  rd_number # latest .Rd number is the number of rounds in a tournament
                #rounds = 0 # cant be null 
                players.append(player)
                

            return rankings 
            
    def get_sim_dict(self): # returns the dictionary of x where key is id and value is points
        

        tournament = self.main_window.get_current_tournament()
        players = tournament.players


        x_dict = {}
        x_id = [] # stores the ids,
        x_score = []
        
        for p in players: 


            # put the label into the item
            
            x_dict[p.id] = p.points
            x_id.append(p.id)# appends the ids according to the rank
            x_score.append(p.points)
            
            

        return x_dict #ids in same order as get actual dict function
    
    def sort_sim_dict(self): # sort by dict value. this means the key is the id and index would be position in the tournament
        
        x_dict = self.get_sim_dict() 
        
        sorted_dict = dict(sorted(x_dict.items(), key=lambda item: item[1]))
        
        return sorted_dict # sort by points
    
    def sort_actual_dict(self): # sort actual dict by value
        
        y_dict = self.get_actual_dict() 
        
        sorted_dict = dict(sorted(y_dict.items(), key=lambda item: item[1]))
        
        return sorted_dict
    
    def sort_dict_by_value(self, input_dict): # generic function to sort a dictionary by value
        sorted_dict = dict(sorted(input_dict.items(), key=lambda item: item[1]))
        return sorted_dict
    
    
    def get_aroc(self, player): # returns the aroc for a player in the current tournament
        aroc = round(self.main_window.tie_break_controller.calculate_aroc(player),2) # round aroc to 2 decimal places
        
        return aroc
    
    def get_all_arocs(self): # returns a dictionary of player id and their aroc for al players in the current tournament
        tournament = self.main_window.get_current_tournament()
        players = tournament.players
        aroc_dict = {}
        for p in players:
            aroc = self.get_aroc(p)
            aroc_dict[p.id] = aroc
        return aroc_dict
    
    def get_buchholz(self, player): # returns the buchholz for a player in the current tournament
        buchholz = self.main_window.tie_break_controller.calculate_buchholz(player)
        
        return buchholz
    
    def get_all_buchholz(self): # returns a dictionary of player id and their buchholz for al players in the current tournament
        tournament = self.main_window.get_current_tournament()
        players = tournament.players
        buchholz_dict = {}
        for p in players:
            buchholz = self.get_buchholz(p)
            buchholz_dict[p.id] = buchholz
        return buchholz_dict #ids in same order as get_actual_dict function
    
    def get_sonneborn_berger(self, player): # returns the sonneborn berger for a player in the current tournament
        sonneborn_berger = self.main_window.tie_break_controller.calculate_sonneborn_berger(player)
        
        return sonneborn_berger
    
    def get_all_sonneborn_berger(self): # returns a dictionary of player id and their sonneborn berger for al players in the current tournament
        tournament = self.main_window.get_current_tournament()
        players = tournament.players
        sonneborn_berger_dict = {}
        for p in players:
            sonneborn_berger = self.get_sonneborn_berger(p)
            sonneborn_berger_dict[p.id] = sonneborn_berger
        return sonneborn_berger_dict
    
        
    def add_to_results_listbox(self):
        tournament = self.main_window.get_current_tournament()
        players = tournament.players

        # Sort by points
        players_sorted = sorted(players, key=lambda p: p.points, reverse=True)

        self.main_window.results_listbox.clear()
       
        
        
        
        for p in players_sorted: 
            p.aroc = self.get_aroc(p)
            p.buchholz = self.get_buchholz(p)
            p.sonneborn_berger = self.get_sonneborn_berger(p)
            summary_label = QLabel(f"{p.id}) {p.name} - {p.points}, Buchholz: {p.buchholz}, Sonneborn-Berger: {p.sonneborn_berger}, AROC: {p.aroc}") 
            item = QListWidgetItem()

            self.main_window.results_listbox.addItem(item)

            # put the label into the item
            self.main_window.results_listbox.setItemWidget(item, summary_label)
            
            
             
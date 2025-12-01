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
        
        # in the dictionaries below x_dict and y_dict will have the ids at the same key indexes. This allows the score to account for ties
        
        x_dict = self.get_sim_dict()
        x_id = list( x_dict.keys())    
        x_score = list(x_dict.values())    
            

        y_dict = self.get_actual_dict()
        y_id =list( y_dict.keys())
        y_score = list(y_dict.values())
        
        print("simulation ids", x_id)
        print("sim values", x_score)
        
        print("actual ids",y_id)
        print("actual scores,", y_score)

        sim_ranks = stats.rankdata([-s for s in x_score], method='average')  # negative to rank descending actual ranks
        actual_ranks = stats.rankdata([-s for s in y_score], method='average')
        
      
        tau, p_value = kendalltau(sim_ranks, actual_ranks)
        print("Kendall tau:", tau)
        print("p-value:", p_value)
        self.main_window.submit_results_controller.clear_layout(self.main_window.stats_groupbox_layout)
        
        
        
        sim_tau_label = QLabel(f"Kendall Tau with ties:{tau}")
        sim_p_label=QLabel(f"P_value{p_value}")
        self.main_window.stats_groupbox_layout.addWidget(sim_tau_label)
        self.main_window.stats_groupbox_layout.addWidget(sim_p_label)
        
        
        x_sorted_sim_dict = self.sort_sim_dict()
        x_sorted_ids = list(x_sorted_sim_dict.keys())
        
        y_sorted_actual_dict = self.sort_actual_dict()
        y_sorted_ids = list(y_sorted_actual_dict.keys())
        
        
        tau, p_value = kendalltau(x_sorted_ids, y_sorted_ids) # program forced to rank tied values
        print("Kendall tau:", tau)
        print("p-value:", p_value)        
        
        
        sim_tau_label = QLabel(f"Kendall Tau with no ties:{tau}")
        sim_p_label = QLabel(f"P_value{p_value}")
        self.main_window.stats_groupbox_layout.addWidget(sim_tau_label)
        self.main_window.stats_groupbox_layout.addWidget(sim_p_label)
        
        self.add_to_results_listbox() # outputs players to results listbox sorted by points
        
        
        
        
        

        
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
            for i, row in self.df.iterrows():
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
                

            #y = sorted(rankings, key=rankings.get, reverse=True) # sort players by points, return the ids
            return rankings
            
    def get_sim_dict(self): # get the dictionary of x where key is id and value is points
        

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
            
            

        return x_dict
    
    def sort_sim_dict(self): # sort by dict value. this means the key is the id and index would be position in the tournament
        
        x_dict = self.get_sim_dict() 
        
        sorted_dict = dict(sorted(x_dict.items(), key=lambda item: item[1]))
        
        return sorted_dict
    
    def sort_actual_dict(self): # sort actual dict by value
        
        y_dict = self.get_actual_dict() 
        
        sorted_dict = dict(sorted(y_dict.items(), key=lambda item: item[1]))
        
        return sorted_dict
        
        
    def add_to_results_listbox(self):
        tournament = self.main_window.get_current_tournament()
        players = tournament.players

        # Sort by points
        players_sorted = sorted(players, key=lambda p: p.points, reverse=True)

        self.main_window.results_listbox.clear()
       
        
        
        
        for p in players_sorted: 
            summary_label = QLabel(f"{p.id}) {p.name} - {p.points}") 
            item = QListWidgetItem()

            self.main_window.results_listbox.addItem(item)

            # put the label into the item
            self.main_window.results_listbox.setItemWidget(item, summary_label)
            
            
             
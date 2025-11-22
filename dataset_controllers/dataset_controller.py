

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from models.tournament import Tournament
from models.player import Player
import pandas as pd

class DatasetController:
    def __init__(self, main_window):
            self.main_window = main_window

    def import_players_from_dataset(self):
            try:
                # Build the full correct path
                path = f"Datasets/Grand swiss.csv"

                # Read the CSV, splitting on tabs
                self.df = pd.read_csv(path, sep="\t", engine="python")
            except Exception as e:
                print("Error loading CSV:", e)
                return

            # clean columns
            self.df.columns = self.df.columns.str.strip()

            print("Columns:", self.df.columns.tolist())
            players = []
            
            for i, row in self.df.iterrows():
                name = row["Name"]
                rating = row["Rtg"]
                federation = row["FED"]
                points = row["Pts."]
                player = Player(i+1,name,rating)
                players.append(player)

                print(name, rating, federation, points)

            tournamentId = self.main_window.tournament_controller.get_current_tournament_id()
            tournament = Tournament(tournamentId,"Grand swiss.csv",players,None,None,None)
            self.main_window.tournaments["Grand swiss.csv"] = tournament #This creates a key in the dictionary   
            self.main_window.tournament_controller.add_button_to_tournament_group("Grand swiss.csv") # create the button and change current tournament id

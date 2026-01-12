

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from models.tournament import Tournament
from models.player import Player
import pandas as pd
import re

class DatasetController:
    def __init__(self, main_window):
            self.main_window = main_window

    def import_players_from_dataset(self,file):
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
            for i, row in self.df.iterrows():
                name = row["Name"]
                rating = row["Rtg"]
                federation = row["FED"]
                #points = row["Pts."]
                id = row["No."]
                player = Player(id,name,rating)
                for col in self.df.columns:
                    if col.endswith(".Rd"):
                        rd_number = int(col.split(".Rd")[0]) # gets the latest .Rd number
                    
            

                rounds =  rd_number # latest .Rd number is the number of rounds in a tournament
                #rounds = 0 # cant be null 
                players.append(player)

                #print(name, rating, federation, points)
            
            tournamentId = self.main_window.tournament_controller.get_current_tournament_id()
            next_player_id = len(players) + 1 # update next player id
            tournament = Tournament(tournamentId,file,players,None,rounds)
            tournament.next_player_id = next_player_id
            self.main_window.tournaments[file] = tournament #This creates a key in the dictionary   
            self.main_window.tournament_controller.add_button_to_tournament_group(file) # create the button and change current tournament id

    def import_players_from_all_datasets(self):
        import glob

        folder = "Datasets"

        csv_files = glob.glob(f"{folder}/*.csv")

        print("Number of CSV files:", len(csv_files))
        print("CSV files:")
        
        files_skipped = []
        for file in csv_files:
            tournaments = self.main_window.tournaments  # get all the tournaments
            if file in tournaments:
                print(f"Tournament '{file}' already exists. Skipping import.")
                files_skipped.append(file)
            else:
                self.import_players_from_dataset(file)
        if files_skipped:
            QMessageBox.warning(self.main_window, "Files skipped", f'files skipped due to duplicates: {files_skipped}')

        
    def apply_scores_in_dataset(self):
        tournament = self.main_window.get_current_tournament()
        path = self.find_dataset_file()
        self.df = pd.read_csv(path, sep="\t", engine="python")
        
        
        
        current_round = tournament.current_round
        file_col = str(current_round) +".Rd"

        for i, row in self.df.iterrows():
            name = row["Name"]
            data = row[file_col]
            id = row["No."]
        
            oppid,colour,score = self.split_data(data)
            self.apply(id,oppid,score)
            
            
            
            
        

    def find_dataset_file(self):
        tournament = self.main_window.get_current_tournament()
        file = tournament.name
        return file
    
    def apply(self, id, oppid, score):
        if id is None or score is None:
            return  # skip invalid rows

        try:
            s = float(score)
        except (ValueError, TypeError):
            print("Skipping invalid score:", score)
            return

        opp_score = 1 - s  # safe now

        row_layouts = self.main_window.submit_results_controller.get_rows_from_layout(
            self.main_window.pairings_scroll_layout
        )

        for row_widget in row_layouts:
            w = self.main_window.submit_results_controller.get_row_widgets(row_widget)
            label1, combo1, combo2, label2 = w

            player1 = self.main_window.find_player_from_name(label1.text())
            player2 = self.main_window.find_player_from_name(label2.text())

            # Format to match QComboBox items
            score_str = self.format_score(s)
            opp_score_str = self.format_score(opp_score)

            if player1.id == id and player2.id == oppid:
                combo1.setCurrentText(score_str)
                combo2.setCurrentText(opp_score_str)
            elif player1.id == oppid and player2.id == id:
                combo2.setCurrentText(score_str)
                combo1.setCurrentText(opp_score_str)

            
            
            
    def format_score(self, score):
        # score may be float like 1.0, 0.0, 0.5
        if score == 0.5:
            return "0.5"
        if score == 1 or score == 1.0:
            return "1"
        if score == 0 or score == 0.0:
            return "0"
        return str(score)  # fallback

    def split_data(self, value):
        """
        Parse strings like '19b½' or '20w0' into (oppid, colour, score).
        Returns (None,None,None) for invalid or missing data.
        """

        if value is None:
            return None, None, None

        text = str(value).strip()

        # Common invalid values
        if text == "" or text.lower() in ["nan", "none", "-", "bye"]:
            return None, None, None

        # Pattern: number + letters + (number OR ½)
        match = re.match(r'^(\d+)([A-Za-z]+)(\d+|½)$', text)

        if not match:
            #print("Skipping invalid data:", text)
            return None, None, None

        oppid = int(match.group(1))
        colour = match.group(2)

        score_raw = match.group(3)

        # Convert "½" to 0.5
        if score_raw == "½":
            score = 0.5
        else:
            score = float(score_raw)

        return oppid, colour, score

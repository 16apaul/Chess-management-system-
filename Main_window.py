
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ui.menu_bar import create_menu_bar
from ui.tournament_tabs import create_tournament_tabs
from ui.tournament_group import create_tournament_group
from controllers.player_controller import PlayerController
from controllers.round_controller import RoundController
from controllers.tournament_controller import TournamentController
from controllers.persistence_controller import PersistenceController
from controllers.pair_players_controller import PairPlayersController
from controllers.submit_results_controller import SubmitResultsController
import pandas as pd
from models.tournament import Tournament
from models.player import Player

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        
        # make main layout grid
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QGridLayout()
        central_widget.setLayout(self.layout)
        self.tournaments = {}  # Dictionary to hold tournament data. key is tournament name, value is Tournament object

        self.setWindowTitle("Chess Manager")
        self.setGeometry(100, 100, 1000, 500)
       
       
       
               
        self.tournament_controller = TournamentController(self)
        self.player_controller = PlayerController(self)
        self.round_controller = RoundController(self)
        self.persistence_controller = PersistenceController(self)
        self.pair_players_controller = PairPlayersController(self)
        self.submit_results_controller = SubmitResultsController(self)
      
        
        
        create_tournament_group(self)# creates a group to hold tournament buttons
        
        create_menu_bar(self)

        create_tournament_tabs(self)



        

    def create_tournament_from_dataset(self):
        import pandas as pd
        print("running")
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

        tournamentId = self.tournament_controller.get_current_tournament_id()
        tournament = Tournament(tournamentId,"Grand swiss.csv",players,None,None,None)
        self.tournaments["Grand swiss.csv"] = tournament #This creates a key in the dictionary
            
            
        self.tournament_controller.add_button_to_tournament_group("Grand swiss.csv") # create the button and change current tournament id




    
    
    def get_current_tournament(self):# gets the tournament currently toggled
        selected_button = self.tournament_buttons.checkedButton()
        if selected_button:
            tournament_name = selected_button.text()
            return self.tournaments.get(tournament_name)
        return None
    
    def set_current_tournament(self, tournament): # changes value in dictionary to update tournament
        old_tournament = self.get_current_tournament()
        if old_tournament:
            self.tournaments[old_tournament.name] = tournament
            
    
            
    
                
        
    


    
    


        
        
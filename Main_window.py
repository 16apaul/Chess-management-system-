
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
from dataset_controllers.dataset_controller import DatasetController
from controllers.simulation_contoller import SimulationController
from controllers.end_tournament_controller import EndTournamentController
from controllers.tie_break_controller import TieBreakController
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
        self.setGeometry(100, 100, 1500, 1000)
       
       
       
               
        self.tournament_controller = TournamentController(self)
        self.player_controller = PlayerController(self)
        self.round_controller = RoundController(self)
        self.persistence_controller = PersistenceController(self)
        self.pair_players_controller = PairPlayersController(self)
        self.submit_results_controller = SubmitResultsController(self)
        self.dataset_controller = DatasetController(self)
        self.simulation_controller = SimulationController(self)
        self.end_tournament_controller = EndTournamentController(self)
        self.tie_break_controller = TieBreakController(self)
        create_tournament_group(self)# creates a group to hold tournament buttons
        
        create_menu_bar(self)

        create_tournament_tabs(self)



    
    def find_player_from_id(self,id):
        tournament = self.get_current_tournament()
        players = tournament.players
        for player in players:
            if player.id == id:
                return player
        
    def find_player_from_name(self,name):
        tournament = self.get_current_tournament()
        players = tournament.players
        
        for player in players:
            if player.name == name:
                return player

    
    
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
            
    
            
    
                
        
    


    
    


        
        
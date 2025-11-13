
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ui.menu_bar import create_menu_bar
from ui.tournament_tabs import create_tournament_tabs
from ui.tournament_group import create_tournament_group
from controllers.player_controller import PlayerController
from controllers.round_controller import RoundController
from controllers.tournament_controller import TournamentController
from controllers.persistence_controller import PersistenceController
# List available styles
# Output example: ['Windows', 'Fusion', 'Macintosh']

# Set one


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

      
        
        
        create_tournament_group(self)# creates a group to hold tournament buttons
        
        create_menu_bar(self)

        create_tournament_tabs(self) 
    
        
        
    def pair_players(self):
        
        round_listbox = self.round_listbox
        tournament_listbox = self.tournament_listbox
        tournament = self.get_current_tournament()
        round_players = tournament.players_in_current_round
        tournament_players = tournament.players

        
        for player in tournament_players:
            player.add_half_bye_history(player.has_half_bye) # add a half bye to half bye history
            player.has_half_bye = False # set half bye to false
            
            
        for player in round_players: # go through every rouund player
            player.has_played = True # set every player has played to true
            
            
        
        # update player ID's in tournament
        
        
        
        
        if tournament.current_round == 0: # first round gets paired diferently than the others
            pass
       
       
       
       
       
        round_players.clear() # clears players in round list in tournament
        round_listbox.clear() # clears the list box
        
        # runs when pairings are finished
        tournament.increment_current_round() # increment after round is finished
        self.set_current_tournament(tournament) # saves the tournament.
        
        tournament_listbox.clear()
        for player in tournament.players: # update the listbox
            self.player_controller.add_player_to_tournament_listbox(player)
            
        
            


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
            
    
            
    
                
        
    


    
    


        
        
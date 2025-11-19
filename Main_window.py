
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

      
        
        
        create_tournament_group(self)# creates a group to hold tournament buttons
        
        create_menu_bar(self)

        create_tournament_tabs(self) 
    
    
    def clear_layout(self,layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)

                # If the item is a widget, delete it
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()

                # If the item is a layout, clear it recursively
                else:
                    child_layout = item.layout()
                    if child_layout is not None:
                        self.clear_layout(child_layout)
                        
    def submit_results(self):
        
        row_layouts = self.get_rows_from_layout(self.pairings_scroll_layout)
        for row in row_layouts:
            w = self.get_row_widgets(row)

            label1 = w[0]      # QLabel
            combo1 = w[1]      # QComboBox
            combo2 = w[2]      # QComboBox
            label2 = w[3]      # QLabel

            print(label1.text(), combo1.currentText(), combo2.currentText(), label2.text())
            
        self.clear_layout(self.pairings_scroll_layout)
            
            
    
    
    def get_row_widgets(self,row_layout):
        widgets = []
        for i in range(row_layout.count()):
            w = row_layout.itemAt(i).widget()
            if w:
                widgets.append(w)
        return widgets
    
    def get_rows_from_layout(self, layout):
        row_layouts = []
        for i in range(layout.count()):
            item = layout.itemAt(i)

            if item.layout():
                row_layouts.append(item.layout())


        return row_layouts
    
    
        

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
            
    
            
    
                
        
    


    
    


        
        
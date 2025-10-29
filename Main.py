import sys
from tournament import Tournament
from player import Player
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


# List available styles
# Output example: ['Windows', 'Fusion', 'Macintosh']

# Set one
tournaments = [] # List to hold tournament data
tournament_id = 1  # counter for tournament IDs  



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
        self.setGeometry(100, 100, 400, 300)
       
       
        # create button group box for tournaments
        self.tournament_groupbox = QGroupBox("Tournaments", self) # Group box to hold tournament buttons
        self.layout.addWidget(self.tournament_groupbox, 0, 0)
        self.tournament_layout = QVBoxLayout()  
        self.tournament_layout.setAlignment(Qt.AlignTop)  # Align buttons to the top
        self.tournament_groupbox.setLayout(self.tournament_layout)
        self.tournament_buttons_list = []  # List to hold tournament buttons
        
        # make the tournament buttons toggleable
        self.tournament_buttons = QButtonGroup(self)
        self.tournament_buttons.setExclusive(True)  # Only one button can be checked at a time
        self.tournament_buttons.buttonClicked.connect(self.on_tournament_selected)
               
        
      
        
        
        
        
        
        
        self.tournament_tabs_ui()
        self.menu_ui()
        

        
        
        
        
        
        
        
    def tournament_tabs_ui(self):
              #  tabs to the window layout
        
    
        self.tournament_tabs = QTabWidget() 
        self.layout.addWidget(self.tournament_tabs, 0, 1, 1, 3) # spans add to main layout spans three columns
        add_player_tab = QWidget()
        add_player_tab_layout = QGridLayout()
        add_player_tab.setLayout(add_player_tab_layout)
        
        
        
        self.add_player_listbox = QListWidget() #box to show list of players and add players to tournament
        add_player_tab_layout.addWidget(self.add_player_listbox, 0, 0, 1,2)
        self.add_player_listbox.setSelectionMode(QListWidget.MultiSelection) # allow multiple selection of players
        
        
        self.add_player_lineedit = QLineEdit()
        self.add_player_lineedit.setPlaceholderText("Player name")
        add_player_tab_layout.addWidget(self.add_player_lineedit, 4, 0)
        self.add_player_rating_lineedit = QLineEdit()
        self.add_player_rating_lineedit.setPlaceholderText("Player rating")
        add_player_tab_layout.addWidget(self.add_player_rating_lineedit, 4, 1)
        add_player_button = QPushButton("Add Player") # button to add player to tournament
        add_player_tab_layout.addWidget(add_player_button, 5, 0,1,1)
        add_player_button.clicked.connect(self.add_player_to_tournament) 
        delete_player_button = QPushButton("Delete Player") # button to delete selected player from tournament
        add_player_tab_layout.addWidget(delete_player_button, 5, 1,1,1)
        
        
        add_all_players_to_round_button = QPushButton("Add all") # button to add all players to the current round
        add_player_tab_layout.addWidget(add_all_players_to_round_button, 0, 2)
        
        add_selected_players_to_round_button = QPushButton("-->") # button to add selected players to the current round
        add_player_tab_layout.addWidget(add_selected_players_to_round_button, 2, 1,2,1)
        
        remove_selected_players_from_round_button = QPushButton("<--") # button to remove selected players from the current round
        add_player_tab_layout.addWidget(remove_selected_players_from_round_button, 2, 3,2,1)
        
        round_listbox = QListWidget() # box to show list of round players
        add_player_tab_layout.addWidget(round_listbox, 0, 3, 1,2)
        round_listbox.setSelectionMode(QListWidget.MultiSelection) # allow multiple selection of players
        
        pair_button = QPushButton("Pair Round") # button to pair the current round
        add_player_tab_layout.addWidget(pair_button, 4, 3,1,1)
        
        
        
        
        pairings_tab = QWidget()
        results_tab = QWidget()
        
        self.tournament_tabs.addTab(add_player_tab, "Add Players")
        self.tournament_tabs.addTab(pairings_tab, "Pairings")
        self.tournament_tabs.addTab(results_tab, "Results")
        self.tournament_tabs.hide()  # Hide tabs initially
        
        
    def add_player_to_tournament(self): # what happens when add player button is clicked

        player_name = self.add_player_lineedit.text()
        player_rating = self.add_player_rating_lineedit.text()
        player_listbox = self.add_player_listbox
        tournament = self.tournaments.get(self.tournament_buttons.checkedButton().text())
        print(tournament)
        if player_name:
            try:
                rating = int(player_rating) if player_rating else None
                
                
            except ValueError:
                rating = None
              
              
            next_player_id = tournament.next_player_id #current next player id
            player_id = next_player_id
            player = Player(player_id, player_name, rating)
            
            
            
            # Add player to listbox
            if rating is not None:
                player_listbox.addItem(f"{player_id}) {player.name} (Rating: {player.rating})")
            else:
                player_listbox.addItem(f"{player_id}) {player.name}")
                
            # Update tournament's next player ID
            tournament.next_player_id += 1
            tournament.add_player(player)  # Add player to tournament's player list

            self.tournaments[self.tournament_buttons.checkedButton().text()] = tournament # Update the tournament in the dictionary

            # Clear input fields
            self.add_player_lineedit.clear()
            self.add_player_rating_lineedit.clear()
          
          
          
    def menu_ui(self):
        # Create a menu bar
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        # actions for the File menu
        new_action = QAction("save", self)
        open_action = QAction("Open", self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # Create Tournament menu
        tournament_menu = menubar.addMenu("Tournament") # add menu
        create_tournament_action = QAction("Create Tournament", self) # create items for the menu
        delete_tournament_action = QAction("Delete Tournament", self)
        
        tournament_menu.addAction(create_tournament_action) # link menu to items
        tournament_menu.addAction(delete_tournament_action)



        create_tournament_action.triggered.connect(self.create_tournament) 
        delete_tournament_action.triggered.connect(self.delete_tournament)
    
    def load_tournament(self):
        tournament = self.tournaments.get(self.tournament_buttons.checkedButton().text())
        self.add_player_listbox.clear()
        for player in tournament.players:
            if player.rating is not None:
                self.add_player_listbox.addItem(f"{player.id}) {player.name} (Rating: {player.rating})")
            else:
                self.add_player_listbox.addItem(f"{player.id}) {player.name}")

    
    
    def delete_tournament(self): # what happens when menu delete tournament button is clicked
        selected_button = self.tournament_buttons.checkedButton()
        if selected_button:
            tournament_name = selected_button.text()
            confirm = QMessageBox.question(
                self,
                "Delete Tournament",
                f"Are you sure you want to delete the tournament '{tournament_name}'?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if confirm == QMessageBox.Yes:
                # Remove from layout and button group
                self.tournament_layout.removeWidget(selected_button) # remove from layout
                self.tournament_buttons.removeButton(selected_button) # remove from button group
                selected_button.deleteLater()  # Remove the button from the UI
                self.tournament_buttons_list.remove(selected_button)  # Remove from the list

                # Remove from data structures
                if tournament_name in self.tournaments:
                    del self.tournaments[tournament_name] # remove from dictionary
                global tournaments
                tournaments = [t for t in tournaments if t.name != tournament_name] # remove from list
                if self.tournament_buttons.checkedButton() is None:
                    self.tournament_tabs.hide()  # Hide tabs if no tournament is selected
        else:
            QMessageBox.warning(self, "No Selection", "Please select a tournament to delete.")



    def create_tournament(self): # what happens when menu create tournament button is clicked
        
        
        tournament_round = None
        
        
        tournament_name, ok_name = QInputDialog.getText( #input dialog to get tournament name
            self, "Tournament Name", "Enter tournament name:", QLineEdit.Normal, "Spring Open",
        )
        tournament_type, ok_type = QInputDialog.getItem( #input dialog to get tournament type
            self, "Tournament Type", "Select tournament type:", ["Swiss", "Round Robin", "Knockout"],0, False
        )
        
        if tournament_type == "Swiss": # if swiss, get number of rounds
            tournament_round, ok_round = QInputDialog.getInt(
                self, "Number of Rounds", "Enter number of rounds:", min=1,
            )
        
        
        

        repeat_names = False
        ok = ok_name and ok_type and (tournament_type != "Swiss" or ok_round)
        for t in tournaments:
            if t.name == tournament_name:
                repeat_names = True
                break
        if ok and tournament_name and not repeat_names:
            tournament_button = QPushButton(tournament_name)
            tournament_button.setCheckable(True)
            self.tournament_layout.addWidget(tournament_button)
            self.tournament_buttons.addButton(tournament_button) # this button group makes the buttons toggleable
            self.tournament_buttons_list.append(tournament_button)  # Add button to the list
            global tournament_id
        
            tournament = Tournament(tournament_id, tournament_name,None,tournament_type,tournament_round) # Create a new Tournament object
            
            tournaments.append(tournament)
            
            self.tournaments[tournament_name] = tournament #This creates a key in the dictionary
            button_id = tournament_id  # Capture the current tournament_id
            tournament_button.clicked.connect(lambda checked, name=tournament_name: self.open_tournament(name,button_id))
            tournament_id += 1


        elif  not ok:
            pass  # User cancelled the input dialog
            
        else:
            QMessageBox.warning(self, "Input Error", "Tournament name cannot be empty and must be unique.")
        
    def open_tournament(self, name,id): # what happens when a specific tournament button is clicked
        # Add something to this tournament’s array
        self.tournament_tabs.show()  # Show tabs when a tournament is created
        self.load_tournament()
        data = self.tournaments[name]

        print(
            f"Opening Tournament: {name} with ID: {id}"
            "Tournament Data",
            f"Tournament: {name}\nData: {data}"
        )

    def on_tournament_selected(self, button):
        """Triggered when any tournament button is toggled on."""
        selected_name = button.text()
        print(f"Tournament selected: {selected_name}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    
   
    sys.exit(app.exec_())
    
    


        
        
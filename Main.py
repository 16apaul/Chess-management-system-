import sys
from tournament import Tournament
from player import Player
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


# List available styles
# Output example: ['Windows', 'Fusion', 'Macintosh']

# Set one
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
        self.setGeometry(100, 100, 1000, 500)
       
       
        # create button group box for tournaments
        self.tournament_groupbox = QGroupBox("Tournaments", self) # Group box to hold tournament buttons
        self.layout.addWidget(self.tournament_groupbox, 0, 0)
        self.tournament_layout = QVBoxLayout()  
        self.tournament_layout.setAlignment(Qt.AlignTop)  # Align buttons to the top
        self.tournament_groupbox.setLayout(self.tournament_layout)
        
        # make the tournament buttons toggleable
        self.tournament_buttons = QButtonGroup(self)
        self.tournament_buttons.setExclusive(True)  # Only one button can be checked at a time
               
        
      
        
        
        
        
        
        self.menu_ui()

        self.tournament_tabs_ui()
        

        
        
        
        
        
        
        
    def tournament_tabs_ui(self):
              #  tabs to the window layout
        
    
        self.tournament_tabs = QTabWidget() 
        self.layout.addWidget(self.tournament_tabs, 0, 1, 1, 3) # spans add to main layout spans three columns
        add_player_tab = QWidget()
        add_player_tab_layout = QGridLayout()
        add_player_tab.setLayout(add_player_tab_layout)
        
        
        
        self.add_player_listbox = QListWidget() #box to show list of players and add players to tournament
        add_player_tab_layout.addWidget(self.add_player_listbox, 0, 0, 1,1)
        self.add_player_listbox.setSelectionMode(QListWidget.SingleSelection)

        
        
        self.add_player_lineedit = QLineEdit()
        self.add_player_lineedit.setPlaceholderText("Player name")
        add_player_tab_layout.addWidget(self.add_player_lineedit, 1, 0)
        self.add_player_rating_lineedit = QLineEdit()
        self.add_player_rating_lineedit.setPlaceholderText("Player rating")
        add_player_tab_layout.addWidget(self.add_player_rating_lineedit, 2, 0)
        add_player_button = QPushButton("Add Player") # button to add player to tournament
        add_player_tab_layout.addWidget(add_player_button, 3, 0,1,1)
        add_player_button.clicked.connect(self.add_all_player_to_tournament) 
       
        
        
        add_all_players_to_round_button = QPushButton("Add all") # button to add all players to the current round
        add_player_tab_layout.addWidget(add_all_players_to_round_button, 1, 1,1,1)
        add_all_players_to_round_button.clicked.connect(self.add_all_players_to_round)
        
        
        
        
        self.round_listbox = QListWidget() # box to show list of round players
        add_player_tab_layout.addWidget(self.round_listbox, 0, 2, 1,1)
        self.round_listbox.setSelectionMode(QListWidget.NoSelection) # allow multiple selection of players
        
        
        pair_button = QPushButton("Pair Round") # button to pair the current round
        add_player_tab_layout.addWidget(pair_button, 2, 2,1,1)
        pair_button.clicked.connect(self.pair_players)
        
        
        
        
        pairings_tab = QWidget()
        results_tab = QWidget()
        
        self.tournament_tabs.addTab(add_player_tab, "Add Players")
        
        
        pairings_tab = QWidget()
        pairings_tab_layout = QHBoxLayout()
        pairings_tab.setLayout(pairings_tab_layout)
        self.tournament_tabs.addTab(pairings_tab, "Pairings")
        
        self.tournament_tabs.addTab(results_tab, "Results")
        self.tournament_tabs.hide()  # Hide tabs initially
        
        
    def pair_players(self):
        
        round_listbox = self.round_listbox
        round_listbox.clear()
            
    
    def add_all_players_to_round(self):
        tournament = self.get_current_tournament()
        tournament_players = self.get_players_in_current_tournament()
        tournament.players_in_current_round = tournament_players.copy()
        self.round_listbox.clear()
        for player in tournament.players:
            self.add_player_to_round_listbox(player)
            
            
    def give_half_point_bye(self,button, player): # what happens if 1/2 button is toggled
        tournament = self.get_current_tournament()
        
        
        
            
        if button.isChecked():
            player.has_half_bye = True
            print("toggled on \n", player.id) 

        else:
            player.has_half_bye = False
            print("toggle off")
            
        
            
        self.set_current_tournament(tournament)
            
            
                   
    
    def get_players_in_current_tournament(self):
        tournament = self.get_current_tournament()
        players = tournament.players
        return players
    
    def add_all_player_to_tournament(self): # what happens when add player button is clicked
        repeat_names = False
        tournament = self.get_current_tournament()
        player_name = self.add_player_lineedit.text()
        player_rating = self.add_player_rating_lineedit.text()
        players = self.get_players_in_current_tournament()
        
        for p in players:
                if (p.name.upper()) == (player_name.upper()):
                    repeat_names = True
                    QMessageBox.warning(self,"No dublicate name" , "name already exists in the tournament")
                    break
        
        if player_name and repeat_names == False:
            try:
                rating = int(player_rating) if player_rating else None
                
                
            except ValueError:
                rating = None
                
                
            player_id = tournament.next_player_id #current next player id
            
            player = Player(player_id, player_name, rating)
            
            
            
            # Update tournament's next player ID
            tournament.next_player_id += 1
            tournament.add_player(player)  # Add player to tournament's player list

            self.set_current_tournament(tournament) # Update the tournament in the main dictionary

            # Clear input fields
            self.add_player_lineedit.clear()
            self.add_player_rating_lineedit.clear()
            
            # Add player to listbox
            self.add_player_to_tournament_listbox(player)

          
          
          
    def delete_player_from_round_list(self, round_listbox, item_widget, playerid): # delete player from round listbox when item is clicked
        # Find and remove the corresponding QListWidgetItem
    
        tournament = self.get_current_tournament()
        
        round_players = tournament.players_in_current_round

        for player in round_players:
            if playerid == player.id:
                round_players.remove(player)
                break
        tournament.players_in_current_round = round_players
        self.set_current_tournament(tournament)

        for i in range(round_listbox.count()):
            list_item = round_listbox.item(i)
            if round_listbox.itemWidget(list_item) == item_widget:
                round_listbox.takeItem(i)
                break
                
        
      
    def delete_player_from_tournament_list(self, list_widget, item_widget, tournament, player): # delete player from tournament listbox and tournament player list when item is clicked
        # Find and remove the corresponding QListWidgetItem
        for i in range(list_widget.count()):
            list_item = list_widget.item(i)
            if list_widget.itemWidget(list_item) == item_widget:
                list_widget.takeItem(i)
             
                round_listbox = self.round_listbox
                # Also remove from round listbox if present 
                for j in range(round_listbox.count()):
                    round_list_item = round_listbox.item(j)
                    round_item_widget = round_listbox.itemWidget(round_list_item)
                    if round_item_widget and round_item_widget.findChild(QLabel).text().startswith(f"{player.id})"):
                        round_listbox.takeItem(j)
                        
                        break
                break

        # Remove player from tournament's player list
        tournament.players.remove(player)
        tournament.players_in_current_round.remove(player)
        self.set_current_tournament(tournament)  # Update the tournament in the main dictionary    
        print(tournament)
        
    def menu_ui(self):

        # Create a menu bar
        

        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        # actions for the File menu
        save_action = QAction("save", self)
        
        open_action = QAction("Open", self)
        
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(save_action)
        
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        save_action.triggered.connect(self.save_tournaments)
        open_action.triggered.connect(self.open_all_tournaments)

        # Create Tournament menu
        tournament_menu = menubar.addMenu("Tournament") # add menu
        create_tournament_action = QAction("Create Tournament", self) # create items for the menu
        delete_tournament_action = QAction("Delete Tournament", self)
        
        tournament_menu.addAction(create_tournament_action) # link menu to items
        tournament_menu.addAction(delete_tournament_action)



        create_tournament_action.triggered.connect(self.create_tournament) 
        delete_tournament_action.triggered.connect(self.delete_tournament)
        
        
    def save_tournaments(self, checked=False):
        import json
        tournaments_data = {}  # dictionary to save

        for name, t in self.tournaments.items():
            tournaments_data[name] = t.to_dict()

        with open("tournaments.json", "w") as f:
            json.dump(tournaments_data, f, indent=4)

        print("Tournaments saved successfully!")
        QMessageBox.information(self, "Saved", "Tournaments saved successfully!")



    def open_all_tournaments(self): # runs when open tournaments is click in the file menu
        import json, os
        if not os.path.exists("tournaments.json"):
            print("No tournaments.json file found — starting fresh.")
            self.tournaments = {}
            return

        with open("tournaments.json", "r") as f:
            data = json.load(f)
            

        self.tournaments = {}  # reset tournaments dictionary

        for name, t_data in data.items():
            # Convert each player dict to a Player object
            players_list = [Player.from_dict(p) for p in t_data.get("players", [])]
            players_in_current_round_list = [Player.from_dict(p) for p in t_data.get("players_in_current_round", [])]
            # Create the Tournament object with Player objects
            tournament = Tournament(
                id=t_data["id"],
                name=t_data["name"],
                players=players_list,  # list of Player objects
                style=t_data.get("style"),
                rounds=t_data.get("rounds"),
                date=t_data.get("date"),
            )
            
            tournament.next_player_id = t_data.get("next_player_id")
            tournament.players_in_current_round = players_in_current_round_list

            # Save in your main dictionary by name
            self.tournaments[name] = tournament

            
        
        print(f"Loaded {self.tournaments} tournaments.")
        
        # Remove buttons from layout and delete them
        while self.tournament_layout.count():
            item = self.tournament_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()  

        # Clear all buttons from the button group
        for button in self.tournament_buttons.buttons():
            self.tournament_buttons.removeButton(button)
            button.deleteLater()
        
        for name in self.tournaments: # creates new buttons and assigned to button group
            self.add_button_to_tournament_group(name)

        
        self.tournament_tabs.hide() # hides the tabs since no tournament is selected when loaded
            

    def add_button_to_tournament_group(self,name): #adds a tournament button
        tournament_button = QPushButton(name)
        tournament_button.setCheckable(True)
        self.tournament_layout.addWidget(tournament_button)
        self.tournament_buttons.addButton(tournament_button) # this button group makes the buttons toggleable
        tournament_button.clicked.connect(self.open_tournament)
        
        latest_tournament = list(self.tournaments.values())[-1] 
        latest_id = latest_tournament.id # get id of most recent tournament
        
        global tournament_id
        tournament_id = latest_id + 1 # set to current id
        
        
        
        
    def load_tournament(self):
        tournament = self.get_current_tournament()
        self.add_player_listbox.clear()
        self.round_listbox.clear()
        for player in tournament.players:
            self.add_player_to_tournament_listbox(player) # adds the ui element
            
        for player in tournament.players_in_current_round:
            self.add_player_to_round_listbox(player) # adds the ui element
          
          
          
    def add_player_to_tournament_listbox(self,player):
        tournament = self.get_current_tournament()
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        player_listbox = self.add_player_listbox

        label_text = f"{player.id}) {player.name}"
        if player.rating is not None:
            label_text += f" (Rating: {player.rating})"

        label = QLabel(label_text)
        
        item_layout.addWidget(label)
        item_layout.addStretch()
        
        # Delete button
        delete_button = QPushButton("❌")
        delete_button.setStyleSheet("QPushButton { border: none; color: red; } QPushButton:hover { background-color: #ffcccc; }")
        item_layout.addWidget(delete_button)
        delete_button.clicked.connect(lambda _, l=player_listbox, it=item_widget: self.delete_player_from_tournament_list(l, it, tournament, player))
        
        
        
        # Create QListWidgetItem
        list_item = QListWidgetItem(self.add_player_listbox)
        list_item.setSizeHint(item_widget.sizeHint())

        
        # Add to list
        self.add_player_listbox.addItem(list_item)
        self.add_player_listbox.setItemWidget(list_item, item_widget)
             
            
    def add_player_to_round_listbox(self,player):
        round_listbox = self.round_listbox
        tournament = self.get_current_tournament()
        print(tournament.players_in_current_round)
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        
        label_text = f"{player.id}) {player.name}"
        if player.rating is not None:
            label_text += f" (Rating: {player.rating})"

        label = QLabel(label_text)
        
        item_layout.addWidget(label)
        item_layout.addStretch()
        
        # 1/2 point bye button
        half_bye_button = QPushButton("½")
        half_bye_button.setToolTip("Assign half-point bye to player")
        half_bye_button.setCheckable(True)
        if player.has_half_bye == True:
            half_bye_button.setChecked(True)
        half_bye_button.setStyleSheet("""
            QPushButton {
                border: 1px solid #ccc;
                border-radius: 5px;
                color: green;
                background-color: white;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #ffe5b4;
            }
            QPushButton:checked {
                background-color: #b2fab4;
                color: black;
                font-weight: bold;
            }
        """)            
        item_layout.addWidget(half_bye_button)
        half_bye_button.toggled.connect(lambda _, b = half_bye_button,p = player: self.give_half_point_bye(b,p))
        
        # Delete button
        delete_button = QPushButton("❌")
        delete_button.setStyleSheet("QPushButton { border: none; color: red; } QPushButton:hover { background-color: #ffcccc; }")
        delete_button.setToolTip("Remove player from round")
        item_layout.addWidget(delete_button)
        delete_button.clicked.connect(lambda _, l=round_listbox, it=item_widget, i = player.id: self.delete_player_from_round_list(l, it,i))
        
        
        # half_bye_button.clicked.connect(lambda _, p=player: self.assign_half_bye(p))
        
        # Create QListWidgetItem
        list_item = QListWidgetItem(round_listbox)
        list_item.setSizeHint(item_widget.sizeHint())

        
        # Add to list
        self.round_listbox.addItem(list_item)
        self.round_listbox.setItemWidget(list_item, item_widget)
        
    
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
                selected_button.deleteLater()  # delete the button widget
            
                # Remove from data structures
                if tournament_name in self.tournaments:
                    self.tournaments.pop(tournament_name) # remove from dictionary
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
        
        tournaments = list(self.tournaments.values())  # Get the list of existing tournaments
        

        repeat_names = False
        ok = ok_name and ok_type and (tournament_type != "Swiss" or ok_round)
        for t in tournaments:
            if t.name == tournament_name:
                repeat_names = True
                break
        if ok and tournament_name and not repeat_names:
            global tournament_id
        
            tournament = Tournament(tournament_id, tournament_name,None,tournament_type,tournament_round) # Create a new Tournament object
            
            
            self.tournaments[tournament_name] = tournament #This creates a key in the dictionary

            self.add_button_to_tournament_group(tournament_name) # create the button and change current tournament id


        elif  not ok:
            pass  # User cancelled the input dialog
            
        else:
            QMessageBox.warning(self, "Input Error", "Tournament name cannot be empty and must be unique.")
            
        
        
    def open_tournament(self): # what happens when a specific tournament button is clicked
        selected_button = self.sender()  # the clicked button
        if selected_button is not None:

            

            tournament = self.get_current_tournament()
            name = tournament.name
            id = tournament.id
            self.tournament_tabs.show()  # Show tabs when a tournament is created
            self.load_tournament()

           # print(
             #   f"Opening Tournament: {name} with ID: {id}"
             #   "Tournament Data",
               # f"\nData: {tournament}"
            #)

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
                
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    
   
    sys.exit(app.exec_())
    
    


        
        
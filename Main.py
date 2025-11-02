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
        add_player_tab_layout.addWidget(self.add_player_listbox, 0, 0, 1,1)
        self.add_player_listbox.setSelectionMode(QListWidget.MultiSelection) # allow multiple selection of players
        
        
        self.add_player_lineedit = QLineEdit()
        self.add_player_lineedit.setPlaceholderText("Player name")
        add_player_tab_layout.addWidget(self.add_player_lineedit, 1, 0)
        self.add_player_rating_lineedit = QLineEdit()
        self.add_player_rating_lineedit.setPlaceholderText("Player rating")
        add_player_tab_layout.addWidget(self.add_player_rating_lineedit, 2, 0)
        add_player_button = QPushButton("Add Player") # button to add player to tournament
        add_player_tab_layout.addWidget(add_player_button, 3, 0,1,1)
        add_player_button.clicked.connect(self.add_player_to_tournament) 
       
        
        
        add_all_players_to_round_button = QPushButton("Add all") # button to add all players to the current round
        add_player_tab_layout.addWidget(add_all_players_to_round_button, 0, 2)
        add_all_players_to_round_button.clicked.connect(self.add_all_players_to_round)
        
        
        add_selected_players_to_round_button = QPushButton("-->") # button to add selected players to the current round
        add_player_tab_layout.addWidget(add_selected_players_to_round_button, 1, 2,1,1)
        
        
        
        self.round_listbox = QListWidget() # box to show list of round players
        add_player_tab_layout.addWidget(self.round_listbox, 0, 3, 2,1)
        self.round_listbox.setSelectionMode(QListWidget.MultiSelection) # allow multiple selection of players
        
        pair_button = QPushButton("Pair Round") # button to pair the current round
        add_player_tab_layout.addWidget(pair_button, 2, 3,1,1)
        
        
        
        
        pairings_tab = QWidget()
        results_tab = QWidget()
        
        self.tournament_tabs.addTab(add_player_tab, "Add Players")
        self.tournament_tabs.addTab(pairings_tab, "Pairings")
        self.tournament_tabs.addTab(results_tab, "Results")
        self.tournament_tabs.hide()  # Hide tabs initially
        
    
    def add_all_players_to_round(self):
        tournament = self.get_current_tournament()
        self.round_listbox.clear()
        round_listbox = self.round_listbox
        for player in tournament.players:
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
            half_bye_button.setStyleSheet("QPushButton { border: none; color: green; } QPushButton:hover { background-color: #ffe5b4; } QPushButton:checked { background-color: #ffe5b4 }")
            item_layout.addWidget(half_bye_button)
            
            # Delete button
            delete_button = QPushButton("❌")
            delete_button.setStyleSheet("QPushButton { border: none; color: red; } QPushButton:hover { background-color: #ffcccc; }")
            delete_button.setToolTip("Remove player from round")
            item_layout.addWidget(delete_button)
            delete_button.clicked.connect(lambda _, l=round_listbox, it=item_widget: self.delete_player_from_round_list(l, it))
            
            
            # half_bye_button.clicked.connect(lambda _, p=player: self.assign_half_bye(p))
            
            # Create QListWidgetItem
            list_item = QListWidgetItem(self.round_listbox)
            list_item.setSizeHint(item_widget.sizeHint())

            
           # Add to list
            self.round_listbox.addItem(list_item)
            self.round_listbox.setItemWidget(list_item, item_widget)
            
    
    def add_player_to_tournament(self): # what happens when add player button is clicked

        player_name = self.add_player_lineedit.text()
        player_rating = self.add_player_rating_lineedit.text()
        player_listbox = self.add_player_listbox
        tournament = self.get_current_tournament()
        
        if player_name:
            try:
                rating = int(player_rating) if player_rating else None
                
                
            except ValueError:
                rating = None
              
              
            next_player_id = tournament.next_player_id #current next player id
            player_id = next_player_id
            player = Player(player_id, player_name, rating)
            
            
            
            # Add player to listbox
            
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            
            label_text = f"{player.id}) {player.name}"
            if player.rating is not None:
                label_text += f" (Rating: {player.rating})"

            label = QLabel(label_text)
            
            item_layout.addWidget(label)
            item_layout.addStretch()
            
            # Delete button
            delete_button = QPushButton("❌")
            delete_button.setStyleSheet("QPushButton { border: none; color: red; } QPushButton:hover { background-color: #ffcccc; }")
            delete_button.setToolTip("Remove player from tournament")
            item_layout.addWidget(delete_button)
            delete_button.clicked.connect(lambda _, l=player_listbox, it=item_widget: self.delete_player_from_tournament_list(l, it, tournament, player))
            
            
            
            # Create QListWidgetItem
            list_item = QListWidgetItem(self.add_player_listbox)
            list_item.setSizeHint(item_widget.sizeHint())

            
           # Add to list
            self.add_player_listbox.addItem(list_item)
            self.add_player_listbox.setItemWidget(list_item, item_widget)
            
                
            # Update tournament's next player ID
            tournament.next_player_id += 1
            tournament.add_player(player)  # Add player to tournament's player list

            self.set_current_tournament(tournament) # Update the tournament in the main dictionary

            # Clear input fields
            self.add_player_lineedit.clear()
            self.add_player_rating_lineedit.clear()
          
          
          
    def delete_player_from_round_list(self, list_widget, item_widget): # delete player from round listbox and tournament player list when item is clicked
        # Find and remove the corresponding QListWidgetItem
        for i in range(list_widget.count()):
            list_item = list_widget.item(i)
            if list_widget.itemWidget(list_item) == item_widget:
                list_widget.takeItem(i)
                
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
        self.set_current_tournament(tournament)  # Update the tournament in the main dictionary    
        print(tournament)
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
        tournament = self.get_current_tournament()
        self.add_player_listbox.clear()
        self.round_listbox.clear()
        player_listbox = self.add_player_listbox
        for player in tournament.players:
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            
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
            tournament_button = QPushButton(tournament_name)
            tournament_button.setCheckable(True)
            self.tournament_layout.addWidget(tournament_button)
            self.tournament_buttons.addButton(tournament_button) # this button group makes the buttons toggleable
            global tournament_id
        
            tournament = Tournament(tournament_id, tournament_name,None,tournament_type,tournament_round) # Create a new Tournament object
            
            
            self.tournaments[tournament_name] = tournament #This creates a key in the dictionary
            tournament_id += 1

            tournament_button.clicked.connect(self.open_tournament)
            


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

            print(
                f"Opening Tournament: {name} with ID: {id}"
                "Tournament Data",
                f"\nData: {tournament}"
            )

    def get_current_tournament(self):
        selected_button = self.tournament_buttons.checkedButton()
        if selected_button:
            tournament_name = selected_button.text()
            return self.tournaments.get(tournament_name)
        return None
    
    def set_current_tournament(self, tournament):
        old_tournament = self.get_current_tournament()
        if old_tournament:
            self.tournaments[old_tournament.name] = tournament
                
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    
   
    sys.exit(app.exec_())
    
    


        
        
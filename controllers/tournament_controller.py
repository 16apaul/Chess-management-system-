
from models.tournament import Tournament
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class TournamentController: # handle how tournament logic
    
    def __init__(self, main_window):
        self.main_window = main_window

    
                
    def add_button_to_tournament_group(self,name): #adds a tournament button
            tournament_button = QPushButton(name)
            tournament_button.setCheckable(True)
            self.main_window.tournament_layout.addWidget(tournament_button)
            self.main_window.tournament_buttons.addButton(tournament_button) # this button group makes the buttons toggleable
            tournament_button.clicked.connect(self.open_tournament)
            
            
            
    def delete_tournament(self): # what happens when menu delete tournament button is clicked
            selected_button = self.main_window.tournament_buttons.checkedButton()
            if selected_button:
                tournament_name = selected_button.text()
                confirm = QMessageBox.question(
                    self.main_window,
                    "Delete Tournament",
                    f"Are you sure you want to delete the tournament '{tournament_name}'?",
                    QMessageBox.Yes | QMessageBox.No,
                )
                if confirm == QMessageBox.Yes:
                    # Remove from layout and button group
                    self.main_window.tournament_layout.removeWidget(selected_button) # remove from layout
                    self.main_window.tournament_buttons.removeButton(selected_button) # remove from button group
                    selected_button.deleteLater()  # delete the button widget
                
                    # Remove from data structures
                    if tournament_name in self.main_window.tournaments:
                        self.main_window.tournaments.pop(tournament_name) # remove from dictionary
                    if self.main_window.tournament_buttons.checkedButton() is None:
                        self.main_window.tournament_tabs.hide()  # Hide tabs if no tournament is selected
            else:
                QMessageBox.warning(self.main_window, "No Selection", "Please select a tournament to delete.")
                
                
        


    def create_tournament(self): # what happens when menu create tournament button is clicked
        
        
        tournament_round = None
        
        
        tournament_name, ok_name = QInputDialog.getText( #input dialog to get tournament name
            self.main_window, "Tournament Name", "Enter tournament name:", QLineEdit.Normal, "Spring Open",
        )
        tournament_type, ok_type = QInputDialog.getItem( #input dialog to get tournament type
            self.main_window, "Tournament Type", "Select tournament type:", ["Swiss", "Round Robin", "Knockout"],0, False
        )
        
        if tournament_type == "Swiss": # if swiss, get number of rounds
            tournament_round, ok_round = QInputDialog.getInt(
                self.main_window, "Number of Rounds", "Enter number of rounds:", min=1,
            )
        
        tournaments = list(self.main_window.tournaments.values())  # Get the list of existing tournaments
        

        repeat_names = False
        ok = ok_name and ok_type and (tournament_type != "Swiss" or ok_round)
        for t in tournaments:
            if t.name == tournament_name:
                repeat_names = True
                break
        if ok and tournament_name and not repeat_names:
            
            tournament_id = self.get_current_tournament_id()
            tournament = Tournament(int(tournament_id), tournament_name,None,tournament_type,tournament_round) # Create a new Tournament object
            self.main_window.tournaments[tournament_name] = tournament #This creates a key in the dictionary
            
            
            self.add_button_to_tournament_group(tournament_name) # create the button and change current tournament id


        elif  not ok:
            pass  # User cancelled the input dialog
            
        else:
            QMessageBox.warning(self.main_window, "Input Error", "Tournament name cannot be empty and must be unique.")
            
        
        
    def open_tournament(self): # what happens when a specific tournament button is clicked
        selected_button = self.main_window.sender()  # the clicked button
        if selected_button is not None:

            
            tournament = self.main_window.get_current_tournament()
            print(tournament)
            
            
            self.main_window.tournament_listbox.clear()
            for player in tournament.players:
                self.main_window.player_controller.add_player_to_tournament_listbox(player) # adds the ui element
                
                
            self.main_window.round_listbox.clear()
            for player in tournament.players_in_current_round:
                self.main_window.round_controller.add_player_to_round_listbox(player) # adds the ui element

    

            tournament = self.main_window.get_current_tournament()
            name = tournament.name
            id = tournament.id
            self.main_window.tournament_tabs.show()  # Show tabs when a tournament is created

           # print(
             #   f"Opening Tournament: {name} with ID: {id}"
             #   "Tournament Data",
               # f"\nData: {tournament}"
            #)
            
            
    def get_current_tournament_id(self):
        tournaments = self.main_window.tournaments  # This is a dict: {name: Tournament}
        
        if not tournaments:
            return 1  # Start from ID 1 if no tournaments exist yet
        
        # Get the highest existing tournament ID which should be last in the list
        latest_tournament = list(tournaments.values())[-1]
        latest_tournament_id = latest_tournament.id
        
        return latest_tournament_id + 1

from models.tournament import Tournament
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from dialog.edit_tournament_dialog import EditTournamentDialog


class TournamentController: # handle how tournament logic
    
    def __init__(self, main_window):
        
        
        self.main_window = main_window

    
                
    def add_button_to_tournament_group(self,name): #adds a tournament button
            tournament_button = QPushButton(name)
            tournament_button.setCheckable(True)
            self.main_window.tournament_layout.addWidget(tournament_button) # add to layout
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
                
                
        

    def edit_tournament(self):

        tournament = self.main_window.get_current_tournament()

        
        selected_button = self.main_window.tournament_buttons.checkedButton()
        if selected_button:
            old_name = tournament.name   

            dialog = EditTournamentDialog(tournament, self.main_window)

            if dialog.exec_() == QDialog.Accepted:
                print("Updated:", tournament.name, tournament.point_system)

                # Update selected button text
                selected_button = self.main_window.tournament_buttons.checkedButton()
                selected_button.setText(tournament.name)

                tournaments = self.main_window.tournaments  # get the dict

                # rename the dict
                if old_name in tournaments:
                    tournaments[tournament.name] = tournaments.pop(old_name) # change the key in the dict

        else:
            QMessageBox.warning(self.main_window, "No Selection", "Please select a tournament to edit.")

            
   
    def create_tournament(self): # what happens when menu create tournament button is clicked
        
        tournament_id = self.get_current_tournament_id()

        tournament = Tournament(int(tournament_id),"spring open",None,"Swiss",0) # Create a new Tournament object  
        dialog = EditTournamentDialog(tournament, self.main_window)

        if dialog.exec_() == QDialog.Accepted: # if user clicks save
            self.main_window.tournaments[tournament.name] = tournament #This creates a key in the dictionary, save tournament object if valid tournament
            
            
            self.add_button_to_tournament_group(tournament.name) # create the button and change current tournament id


        
    def open_tournament(self): # what happens when a specific tournament button is clicked
        selected_button = self.main_window.sender()  # the clicked button
        if selected_button is not None:

            
            tournament = self.main_window.get_current_tournament()
            # print(tournament)
            
            
            self.main_window.tournament_listbox.clear()
            for player in tournament.players: # rebuilds tournament listbox
                self.main_window.player_controller.add_player_to_tournament_listbox(player) # adds the ui element
                
                
            self.main_window.round_listbox.clear()
            for player in tournament.players_in_current_round: # rebuilds round listbox
                self.main_window.round_controller.add_player_to_round_listbox(player) # adds the ui element

            
            self.main_window.submit_results_controller.clear_layout(self.main_window.pairings_scroll_layout) # clear pairings layout
            for white,black in tournament.pairings:
                self.main_window.pair_players_controller.add_pairing_row(white.name, black.name) # rebuild the layout

            self.main_window.submit_results_controller.clear_layout(self.main_window.stats_groupbox_layout) # clear groupbox
                
            
            self.main_window.results_listbox.clear() # clear results
            
            
            tournament = self.main_window.get_current_tournament()
            name = tournament.name
            id = tournament.id
            self.main_window.tournament_tabs.show()  # Show tabs when a tournament is created
            #self.main_window.tournament_tabs.setCurrentIndex(0) # auto change to first tab
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
        
        return latest_tournament_id + 1 # Increment by 1 for new tournament ID
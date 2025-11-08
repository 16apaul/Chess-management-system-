from models.player import Player
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class PlayerController: # handles logic for people to tournaments
    def __init__(self, main_window):
        self.main_window = main_window
        
    def add_player_to_tournament_listbox(self,player):
        tournament = self.main_window.get_current_tournament()
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        player_listbox = self.main_window.add_player_listbox
        
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
        delete_button.clicked.connect(lambda _, l=player_listbox, it=item_widget, p = player: self.delete_player_from_tournament_list(l, it, tournament, p))
        
        
        
        # Create QListWidgetItem
        list_item = QListWidgetItem(self.main_window.add_player_listbox)
        list_item.setSizeHint(item_widget.sizeHint())

        
        # Add to list
        self.main_window.add_player_listbox.addItem(list_item)
        self.main_window.add_player_listbox.setItemWidget(list_item, item_widget)        
        
    
        
        
    def delete_player_from_tournament_list(self, list_widget, item_widget, tournament, player): # delete player from tournament listbox and tournament player list when item is clicked
        # Find and remove the corresponding QListWidgetItem
        for i in range(list_widget.count()):
            list_item = list_widget.item(i)
            if list_widget.itemWidget(list_item) == item_widget:
                list_widget.takeItem(i)
            
                round_listbox = self.main_window.round_listbox
                # Also remove from round listbox if present 
                for j in range(round_listbox.count()):
                    round_list_item = round_listbox.item(j)
                    round_item_widget = round_listbox.itemWidget(round_list_item)
                    if round_item_widget and round_item_widget.findChild(QLabel).text().startswith(f"{player.id})"):
                        round_listbox.takeItem(j) 
                        tournament.players_in_current_round = [
                p for p in tournament.players_in_current_round if p.id != player.id
            ]

                        break
                

        # Remove player from tournament's player list
        tournament.players.remove(player)
        self.main_window.set_current_tournament(tournament)  # Update the tournament in the main dictionary    
        print(tournament)
        
    def add_player_to_tournament(self): # what happens when add player button is clicked 
            repeat_names = False
            tournament = self.main_window.get_current_tournament()
            player_name = self.main_window.add_player_lineedit.text()
            player_rating = self.main_window.add_player_rating_lineedit.text()
            players = self.get_players_in_current_tournament()
            
            for p in players:
                    if (p.name.upper()) == (player_name.upper()):
                        repeat_names = True
                        QMessageBox.warning(self.main_window,"No dublicate name" , "name already exists in the tournament")
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

                self.main_window.set_current_tournament(tournament) # Update the tournament in the main dictionary

                # Clear input fields
                self.main_window.add_player_lineedit.clear()
                self.main_window.add_player_rating_lineedit.clear()
                
                # Add player to listbox
                self.add_player_to_tournament_listbox(player)
                
    def get_players_in_current_tournament(self):
        tournament = self.main_window.get_current_tournament()
        players = tournament.players
        return players
    
                
                
        
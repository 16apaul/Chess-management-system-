from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class RoundController: # handles logic for people to rounds
    def __init__(self, main_window):
        self.main_window = main_window
        
        
    def add_player_to_round_listbox(self,player):
        round_listbox = self.main_window.round_listbox
        
        #tournament = self.get_current_tournament()
        #tournament.add_player_to_current_round(player)

        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        
        label_text = f"{player.id}) {player.name}"
        if player.rating is not None:
            label_text += f" (Rating: {player.rating})"

        label = QLabel(label_text)
        bye_history_str = str(player.half_bye_history)
        label.setToolTip(bye_history_str)

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
        self.main_window.round_listbox.addItem(list_item)
        self.main_window.round_listbox.setItemWidget(list_item, item_widget)
        
        
    def delete_player_from_round_list(self, round_listbox, item_widget, playerid): # delete player from round listbox when item is clicked
        # Find and remove the corresponding QListWidgetItem
    
        tournament = self.main_window.get_current_tournament()
        
        round_players = tournament.players_in_current_round

        for player in round_players:
            if playerid == player.id:
                player.has_half_bye = False # resets the half bye
                round_players.remove(player) # remove corresponding player from round
                break
            
        tournament.players_in_current_round = round_players
        self.main_window.set_current_tournament(tournament)

        for i in range(round_listbox.count()): # remove corresponding listbox item
            list_item = round_listbox.item(i)
            if round_listbox.itemWidget(list_item) == item_widget:
                round_listbox.takeItem(i)
                break
            
    def add_all_players_to_round(self,sim = False): # skip ui updates when sim is True
        
        tournament = self.main_window.get_current_tournament()
        tournament.players_in_current_round = []
        
        if sim:
            for player in tournament.players:
                tournament.add_player_to_current_round(player)
            return
        
        

        self.main_window.round_listbox.clear()
        for player in tournament.players:
            self.add_player_to_round_listbox(player)
            tournament.add_player_to_current_round(player)
            
    def give_half_point_bye(self,button, player): # what happens if 1/2 button is toggled in round listbox
        tournament = self.main_window.get_current_tournament()
            
        if button.isChecked():
            player.has_half_bye = True
            print("toggled on", player.id) 

        else:
            player.has_half_bye = False
            print("toggle off")
            
        
            
        self.main_window.set_current_tournament(tournament)
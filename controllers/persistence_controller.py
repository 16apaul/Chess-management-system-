from models.tournament import Tournament
from models.player import Player
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class PersistenceController: # handles saving and loading tournaments/tournament objects
    def __init__(self, main_window):
        self.main_window = main_window
        
    def save_tournaments(self, checked=False): # what happens when save tournaments is clickedZ
        import json
        tournaments_data = {}  # dictionary to save

        for name, t in self.main_window.tournaments.items():
            tournaments_data[name] = t.to_dict()

        with open("tournaments.json", "w") as f:
            json.dump(tournaments_data, f, indent=4)

        print("Tournaments saved successfully!")
        QMessageBox.information(self.main_window, "Saved", "Tournaments saved successfully!")



    def load_all_tournaments(self): # runs when open tournaments is click in the file menu
        import json, os
        if not os.path.exists("tournaments.json"):
            print("No tournaments.json file found — starting fresh.")
            self.main_window.tournaments = {}
            return

        with open("tournaments.json", "r") as f:
            data = json.load(f)
            

        self.main_window.tournaments = {}  # reset tournaments dictionary

        for name, t_data in data.items():
            # Convert each player dict to a Player object
            players_list = [Player.from_dict(p) for p in t_data.get("players", [])]
            players_in_current_round_list = [Player.from_dict(p) for p in t_data.get("players_in_current_round", [])]
             # Build lookup table for ID → Player object
            id_map = {p.id: p for p in players_list}

            # Rebuild pairings as tuples of Player objects
            pairings = [
                (id_map[white_id], id_map[black_id])
                for white_id, black_id in t_data.get("pairings", [])
            ]
            
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
            tournament.current_round = t_data.get("current_round")
            tournament.pairings = pairings

            # Save in your main dictionary by name
            self.main_window.tournaments[name] = tournament

            
        
        print(f"Loaded {self.main_window.tournaments} tournaments.")
        
        # Remove buttons from layout and delete them
        while self.main_window.tournament_layout.count():
            item = self.main_window.tournament_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()  

        # Clear all buttons from the button group
        for button in self.main_window.tournament_buttons.buttons():
            self.main_window.tournament_buttons.removeButton(button)
            button.deleteLater()
        
        for name in self.main_window.tournaments: # creates new buttons and assigned to button group
            self.main_window.tournament_controller.add_button_to_tournament_group(name)

        
        self.main_window.tournament_tabs.hide() # hides the tabs since no tournament is selected when loaded
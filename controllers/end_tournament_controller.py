from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class EndTournamentController: # when end tournament is clicked
    
    def __init__(self, main_window):
        self.main_window = main_window
        
    
    def end_tournament(self):
        

        tournament = self.main_window.get_current_tournament()
        players = tournament.players

        # Sort by points
        players_sorted = sorted(players, key=lambda p: p.points, reverse=True)

        self.main_window.results_listbox.clear()

        for p in players_sorted:
            summary_label = QLabel(f"{p.id}) {p.name} - {p.points}") 
            item = QListWidgetItem()

            self.main_window.results_listbox.addItem(item)

            # put the label into the item
            self.main_window.results_listbox.setItemWidget(item, summary_label)
            
        self.main_window.submit_results_controller.clear_layout(self.main_window.stats_groupbox_layout)
        tau = 0
        sim_label = QLabel(f"Kendall Tau:{tau}")
        self.main_window.stats_groupbox_layout.addWidget(sim_label)
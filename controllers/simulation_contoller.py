from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
import random

class SimulationController: # assigns scores
    
    def __init__(self, main_window):
        self.main_window = main_window
        
        
    def random_scores(self, sim = False): # assigns random scores to each player
        
        row_layouts = self.main_window.submit_results_controller.get_rows_from_layout(self.main_window.pairings_scroll_layout)     
           
        tournament = self.main_window.get_current_tournament()
        pairings = tournament.pairings
        results = []   # store results here when sim=True
        if sim:
            for pairing in pairings:
                white_player, black_player = pairing

                if random.randint(1, 3) == 1: # 1/3 percent chance white wins
                
                    white_score = 1   # White wins
                    black_score = 0   # Black loses

                elif random.randint(1, 3) == 2: # 1/3 black wins
                    white_score = 0   # White loses
                    black_score = 1   # Black wins

                else: #1/3 it is a draw
                    white_score = 0.5  # White draws
                    black_score = 0.5   # Black draws 
                results.append((white_player, black_player, white_score, black_score))
            return results
        
        for row_widget in row_layouts:
            w = self.main_window.submit_results_controller.get_row_widgets(row_widget)

            combo1 = w[1]      # QComboBox white score            
            
            combo2 = w[2]      # QComboBox Black score
            

            if random.randint(1, 3) == 1: # 1/3 percent chance white wins
                
                combo1.setCurrentIndex(2)   # White wins
                combo2.setCurrentIndex(0)   # Black loses

            elif random.randint(1, 3) == 2: # 1/3 black wins
                combo1.setCurrentIndex(0)   # White loses
                combo2.setCurrentIndex(2)   # Black wins

            else: #1/3 it is a draw
                combo1.setCurrentIndex(1)   # White draws
                combo2.setCurrentIndex(1)   # Black draws
            
        
    def simulate_round_on_rating(self, sim=False):
        tournament = self.main_window.get_current_tournament()
        pairings = tournament.pairings
        results = []   # store results here when sim=True
        if sim:
            for pairing in pairings:
                white_player = pairing[0]
                black_player = pairing[1]
                 # ---- Compute result (same logic) ----
                if abs(white_player.rating - black_player.rating) <= 50:
                    white_score = 0.5   # draw
                    black_score = 0.5
                elif white_player.rating < black_player.rating:
                    white_score = 0   # white loses
                    black_score = 1   # black wins
                else:
                    white_score = 1   # white wins
                    black_score = 0   # black loses   
                results.append((white_player, black_player, white_score, black_score))
            return results

        
        row_layouts = self.main_window.submit_results_controller.get_rows_from_layout(
            self.main_window.pairings_scroll_layout
        )


        for row_widget in row_layouts:
            w = self.main_window.submit_results_controller.get_row_widgets(row_widget)

            label1 = w[0]      # QLabel White name
            combo1 = w[1]      # QComboBox white score
            combo2 = w[2]      # QComboBox Black score
            label2 = w[3]      # QLabel Black name
                
            white_player = self.main_window.submit_results_controller.get_player_from_name(label1.text())
            black_player = self.main_window.submit_results_controller.get_player_from_name(label2.text())

            # ---- Compute result (same logic) ----
            if abs(white_player.rating - black_player.rating) <= 50:
                white_score = 1   # draw
                black_score = 1
            elif white_player.rating < black_player.rating:
                white_score = 0   # white loses
                black_score = 2   # black wins
            else:
                white_score = 2   # white wins
                black_score = 0   # black loses

            # update UI
            if not sim:
                combo1.setCurrentIndex(white_score)
                combo2.setCurrentIndex(black_score)


                
    def simulate_all_rounds(self):

        
        tournament = self.main_window.get_current_tournament()
        current_round = tournament.current_round
        total_rounds = tournament.rounds
        
        
        
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.main_window.setUpdatesEnabled(False)

        for r in range(current_round, total_rounds):
            self.main_window.round_controller.add_all_players_to_round(True)
            self.main_window.pair_players_controller.pair_players(True)
            
            
            #results = self.random_scores(True)
            results = self.simulate_round_on_rating(True)
            self.main_window.submit_results_controller.submit_results(True,results)
            
        self.main_window.end_tournament_controller.end_tournament()
        

        self.main_window.setUpdatesEnabled(True)
        QApplication.restoreOverrideCursor()
 

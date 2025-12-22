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
        point_system = tournament.point_system 
        win = point_system[2]
        draw = point_system[1]
        loss = point_system[0]
        results = []   # store results here when sim=True
        if sim:
            for pairing in pairings:
                white_player, black_player = pairing

                if random.randint(1, 3) == 1: # 1/3 percent chance white wins
                
                    white_score = win   # White wins
                    black_score = loss  # Black loses

                elif random.randint(1, 3) == 2: # 1/3 black wins
                    white_score = loss   # White loses
                    black_score = win   # Black wins

                else: #1/3 it is a draw
                    white_score = draw  # White draws
                    black_score = draw   # Black draws 
                results.append((white_player, black_player, white_score, black_score))
            return results
        
        for row_widget in row_layouts:
            w = self.main_window.submit_results_controller.get_row_widgets(row_widget)

            white_score_combo = w[1]      # QComboBox white score            
            
            black_score_combo = w[2]      # QComboBox Black score
            
            random_number = random.randint(1, 3) # randpm numbers to assign scores
            if  random_number == 1: # 1/3 percent chance white wins
                
                white_score_combo.setCurrentIndex(2)   # White wins
                black_score_combo.setCurrentIndex(0)   # Black loses

            elif random_number == 2: # 1/3 black wins
                white_score_combo.setCurrentIndex(0)   # White loses
                black_score_combo.setCurrentIndex(2)   # Black wins

            else: #1/3 it is a draw
                white_score_combo.setCurrentIndex(1)   # White draws
                black_score_combo.setCurrentIndex(1)   # Black draws
            
        
    def simulate_round_on_rating(self, sim=False): # sim would be true if simulate all rounds are clicked
        tournament = self.main_window.get_current_tournament()
        pairings = tournament.pairings
        point_system = tournament.point_system # list in form [loss,draw,win]
        win = point_system[2] 
        draw = point_system[1]
        loss = point_system[0]
        results = []   # store results here when sim=True
        rating_difference_threshold = 20  # threshold for rating difference to consider a draw
        if sim:
            for pairing in pairings:
                white_player = pairing[0]
                black_player = pairing[1]
                 # ---- Compute result (same logic) ----
                if abs(white_player.rating - black_player.rating) <= rating_difference_threshold: # draw if not much rating difference
                    white_score = draw  # draw
                    black_score = draw
                elif white_player.rating < black_player.rating:
                    white_score = loss   # white loses
                    black_score = win   # black wins
                else:
                    white_score = win   # white wins
                    black_score = loss   # black loses   
                results.append((white_player, black_player, white_score, black_score))
            return results

        
        row_layouts = self.main_window.submit_results_controller.get_rows_from_layout(
            self.main_window.pairings_scroll_layout
        )


        for row_widget in row_layouts:# update combo scores according to the rating for each row
            w = self.main_window.submit_results_controller.get_row_widgets(row_widget)

            white_name_label = w[0]      # QLabel White name
            white_score_combo = w[1]      # QComboBox white score
            black_score_combo = w[2]      # QComboBox Black score
            black_name_label = w[3]      # QLabel Black name
                
            white_player = self.main_window.submit_results_controller.get_player_from_name(white_name_label.text())
            black_player = self.main_window.submit_results_controller.get_player_from_name(black_name_label.text())

            # give draw if not much rating difference
            if abs(white_player.rating - black_player.rating) <= 50:
                white_score = draw   # draw
                black_score = draw
            elif white_player.rating < black_player.rating:
                white_score = loss   # white loses
                black_score = win   # black wins
            else:
                white_score = win  # white wins
                black_score = loss  # black loses   

            # update UI
            
            white_score_combo.setCurrentText(str(white_score))
            black_score_combo.setCurrentText(str(black_score))


                
    def simulate_all_rounds_on_rating(self): # based on rating

        
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
 
    def simulate_all_rounds_randomly(self):

        
        tournament = self.main_window.get_current_tournament()
        current_round = tournament.current_round
        total_rounds = tournament.rounds
        
        
        
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.main_window.setUpdatesEnabled(False)

        for r in range(current_round, total_rounds):
            self.main_window.round_controller.add_all_players_to_round(True)
            self.main_window.pair_players_controller.pair_players(True)
            
            
            results = self.random_scores(True)
            #results = self.simulate_round_on_rating(True)
            self.main_window.submit_results_controller.submit_results(True,results)
            
        self.main_window.end_tournament_controller.end_tournament()
        

        self.main_window.setUpdatesEnabled(True)
        QApplication.restoreOverrideCursor()
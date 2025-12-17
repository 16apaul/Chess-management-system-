from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class TieBreakController: # submit scores and assigns scores
    
    def __init__(self, main_window):
        self.main_window = main_window
        
    def calculate_buchholz(self, player): # calculates buchholz score , sum of opponents' points
        buchholz_score = 0.0

        for opponent_id in player.player_history:
            opponent = self.main_window.find_player_from_id(opponent_id)
            if opponent:
                buchholz_score += opponent.points # points of each opponent played added
        player.buchholz = buchholz_score
        return buchholz_score
    
    
    def calculate_sonneborn_berger(self, player): # calculates sonneborn berger score, 
        tournament = self.main_window.get_current_tournament()
        point_system = tournament.point_system
        win = point_system[2]
        draw = point_system[1]
        loss = point_system[0]
        sonneborn_berger_score = 0.0
        

        for index, opponent_id in enumerate(player.player_history):
            opponent = self.main_window.find_player_from_id(opponent_id)
            if opponent:
                points_against_opponent = player.point_history[index] # points scored against this opponent
                if points_against_opponent == win: # if player won add the opponent's full points
                    sonneborn_berger_score += opponent.points 
                elif points_against_opponent == draw: # if player drew add half the opponent's points
                    sonneborn_berger_score += opponent.points / 2
                    
        player.sonneborn_berger = sonneborn_berger_score
        return sonneborn_berger_score
    
    def calculate_aroc(self, player): # calculates average rating of opponents played
        total_rating = 0
        num_opponents = 0

        for opponent_id in player.player_history:
            opponent = self.main_window.find_player_from_id(opponent_id)
            if opponent and opponent.rating is not None:
                total_rating += opponent.rating
                num_opponents += 1

        if num_opponents == 0:
            return 0.0  # Avoid division by zero

        average_rating = total_rating / num_opponents
        
        player.aroc = average_rating
        return average_rating
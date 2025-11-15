from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class PairPlayersController: # handle how tournament logic
    
    def __init__(self, main_window):
        self.main_window = main_window
        
    def add_pairing_row(self,white,black):
        # Create a horizontal row
        row_layout = QHBoxLayout()

        label1 = QLabel(white)
        combo1 = QComboBox()
        combo1.addItems(["0", "1/2", "1"])
        combo2 = QComboBox()
        combo2.addItems(["0", "1/2", "1"])
        label2 = QLabel(black)

        row_layout.addWidget(label1)
        row_layout.addWidget(combo1)
        row_layout.addWidget(combo2)
        row_layout.addWidget(label2)

        self.main_window.pairings_scroll_layout.addLayout(row_layout)

        
    def pair_players(self):
        
        round_listbox = self.main_window.round_listbox
        tournament_listbox = self.main_window.tournament_listbox
        tournament = self.main_window.get_current_tournament()
        round_players = tournament.players_in_current_round
        tournament_players = tournament.players

        
        for player in tournament_players:
            player.add_half_bye_history(player.has_half_bye) # add a half bye to half bye history
            player.has_half_bye = False # set half bye to false
            
            
        for player in round_players: # go through every round player
            player.has_played = True # set every player has played to true
            
        players_to_be_paired = [] 
        for player in round_players:
            if player.half_bye_history[-1] == False:
                players_to_be_paired.append(player)
               
        
        # update player ID's in tournament
        
        # create the score buckets
        
        self.add_pairing_row("white player", "Black player")
        self.scoring_buckets(players_to_be_paired)
        for player in players_to_be_paired:
            
            pass
        
        
        if tournament.current_round == 0: # first round gets paired differently than the others
            pass
       
       
       
       
       
        round_players.clear() # clears players in round list in tournament
        round_listbox.clear() # clears the list box
        
        # runs when pairings are finished
        tournament.increment_current_round() # increment after round is finished
        self.main_window.set_current_tournament(tournament) # saves the tournament.
        
        tournament_listbox.clear()
        for player in tournament.players: # update the listbox
            self.main_window.player_controller.add_player_to_tournament_listbox(player)
            
        
            
    def get_player_color_score(self,player): # white is 1 black is -1, if color score is 2 they shoud be black next
        color_score = 0
        for color in player.color_history:
            if color == "white":
                color_score += 1
            elif color == "black":
                color_score -= 1
        return color_score
    
    def scoring_buckets(self, players_list): # puts players to be paired in their own scoring bucket
        
        buckets = [] # buckets to track unique scores
        unique_scores = [] # tracking unique scores
        for player in players_list:
            if player.points not in unique_scores:
                unique_scores.append(player.points) # put all unique scores in a list
                
        unique_scores.sort() # sort so first bucket is highest scoring bucket
        
        for _ in unique_scores:
            buckets.append([]) # create the buckets for scores
            
        for player in players_list:
            for i in range(len(unique_scores)):
                if unique_scores[i] == player.points:  # assign the player to the corresponding bucket score
                    buckets[i].append(player)
        print(buckets)
        return buckets
            
            
                
            
            
            
        
        
        
        
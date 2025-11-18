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

        # Reset half-byes and set has_played for this round
        for player in tournament_players:
            player.add_half_bye_history(player.has_half_bye)
            player.has_half_bye = False

        for player in round_players:
            player.has_played = True

        # Players eligible for pairing (no recent half-bye)
        players_to_be_paired = [
            player for player in round_players if not player.half_bye_history[-1]
        ]

        # Handle odd number of players: assign bye to lowest score player without a bye
        
        if len(players_to_be_paired) % 2 == 1:
            # Reverse the list so min() picks the last ranked player if multiple have lowest score
            reversed_players = list(reversed(players_to_be_paired))
            
            try:
                lowest_scoring_player = min(
                    (p for p in reversed_players if not p.has_full_bye),
                    key=lambda x: x.points
                )
                
                lowest_scoring_player.has_full_bye = True
                lowest_scoring_player.points_increment(1)
                
                players_to_be_paired.remove(lowest_scoring_player)
                print(f"{lowest_scoring_player.name} gets a bye this round.")
            except ValueError:
                # Handle the case when no player is eligible for a bye
                print("No eligible player for a bye this round.")
                lowest_scoring_player = None

            
            

        
        
        
        
        
        
        # Create score buckets

        score_buckets = self.scoring_buckets(players_to_be_paired)
        all_players_flat = [p for b in score_buckets for p in b]
        if not self.valid_pairings_exist(all_players_flat):
            print("No valid pairings possible this round!")
            return
            
        valid_score_buckets = self.valid_buckets(score_buckets)


        # Flatten all buckets for final Swiss pairing

       

        # Generate final pairings
        
        if tournament.current_round == 0: # first round paired differently
            alternate_color = 0
            for bucket in valid_score_buckets:
                bucket_pairings = self.swiss_pairing(bucket) # pairings generated disregards color
                for p1, p2 in bucket_pairings:
                    if alternate_color % 2 == 0:
                        self.add_pairing_row(p1.name, p2.name)
                        
                    else:
                        self.add_pairing_row(p2.name, p1.name)
                    alternate_color+=1
                    
                    
                    
                    
        else:
            for bucket in valid_score_buckets:
                bucket_pairings = self.swiss_pairing(bucket) # pairings generated disregards color
                for p1, p2 in bucket_pairings:
                    self.add_pairing_row(p1.name, p2.name)
                        
            
        # Add pairings to UI
        #self.add_pairing_row("White player", "Black player")
        #for p1, p2 in pairings:
            #self.add_pairing_row(p1.name, p2.name)

        # Clear round listbox and round players
        round_players.clear()
        round_listbox.clear()

        # Increment round and update tournament
        tournament.increment_current_round()
        self.main_window.set_current_tournament(tournament)

        # Refresh tournament listbox
        tournament_listbox.clear()
        for player in tournament.players:
            self.main_window.player_controller.add_player_to_tournament_listbox(player)

            
    def valid_buckets(self, score_buckets): # makes sure valud pairings exist for every bucket
        """
        Recursively balance score buckets to ensure:
        - Each bucket has even number of players
        - Valid pairings exist within each bucket
        """
        for b_index in range(len(score_buckets) - 1):
            bucket = score_buckets[b_index]

            # If bucket is empty, skip
            if not bucket:
                continue

            # 1️⃣ Odd bucket → move 1 player to next bucket
            if len(bucket) % 2 == 1:
                moved = False
                for i in reversed(range(len(bucket))):
                    player = bucket.pop(i)
                    score_buckets[b_index + 1].insert(0, player)

                    if self.valid_pairings_exist(bucket):
                        moved = True
                        # Recurse to ensure next buckets are balanced
                        score_buckets = self.valid_buckets(score_buckets)
                        break
                    else:
                        # Undo move if invalid
                        score_buckets[b_index + 1].remove(player)
                        bucket.insert(i, player)

                if not moved:
                    print(f"No valid player to move from bucket {b_index} (odd bucket)! Moving all players down.")
                    all_players = bucket.copy()
                    bucket.clear()
                    score_buckets[b_index + 1] = all_players + score_buckets[b_index + 1]
                    # Recurse after moving all
                    score_buckets = self.valid_buckets(score_buckets)
                    return score_buckets # stop further loop since recursion will handle the rest

            # Even bucket but no valid pairings
            elif not self.valid_pairings_exist(bucket):
                print(f"No valid player to Pair from bucket {b_index} (Even bucket)! Moving all players down.")
                all_players = bucket.copy()
                bucket.clear()
                score_buckets[b_index + 1] = all_players + score_buckets[b_index + 1]
                # Recurse after moving all
                score_buckets = self.valid_buckets(score_buckets)
                return score_buckets
        return score_buckets
   
    def valid_pairings_exist(self, players):
   
        if not players:
            return True

        player = players[0]

        for i in range(1, len(players)):
            opponent = players[i]
            if opponent in player.player_history:
                continue

            remaining = players[1:i] + players[i+1:]
            if self.valid_pairings_exist(remaining):
                return True

        return False


    def swiss_pairing(self,players):
        """
        Creates Swiss-style pairings: top half vs bottom half
        Returns a list of tuples (player1, player2)
        """
        # Sort players by score descending
        players = sorted(players, key=lambda p: p.points, reverse=True)

        # Handle odd number of players by giving a bye to the lowest score player
        if len(players) % 2 == 1:
            bye_player = players.pop(-1)
            print(f"{bye_player} gets a bye this round.")

        # Split top half vs bottom half
        mid = len(players) // 2
        top_half = players[:mid]
        bottom_half = players[mid:]

        # Try to find valid pairings
        def backtrack(top, bottom, current_pairings):
            if not top:
                
                return current_pairings  # all paired successfully

            player = top[0]

            for i, opponent in enumerate(bottom):
                if opponent in player.player_history:
                    continue

                new_top = top[1:]
                new_bottom = bottom[:i] + bottom[i+1:]
                result = backtrack(new_top, new_bottom, current_pairings + [(player, opponent)])
                if result is not None:
                    return result  # found valid pairing

            return None  # no valid pairing possible

        final_pairings = backtrack(top_half, bottom_half, [])

        if final_pairings is None:
            print("No valid pairings possible for this round!")
            return []

        return final_pairings

    
    
    
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
        #print(buckets)
        return buckets
            
            
                
            
            
            
        
        
        
        
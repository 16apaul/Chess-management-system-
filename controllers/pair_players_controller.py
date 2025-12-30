from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class PairPlayersController: # handle how tournament logic
    
    def __init__(self, main_window):
        self.main_window = main_window
        
    def add_pairing_row(self, white_name, black_name):
        tournament = self.main_window.get_current_tournament()
        point_system = tournament.point_system

        point_system = list(map(str, point_system)) # convert point system to string

        row_layout = QHBoxLayout()

        white_name_label = QLabel(white_name)

        white_score_combo = QComboBox()
        white_score_combo.addItems(point_system)
        white_score_combo.setFixedWidth(50)
        white_score_combo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        black_score_combo = QComboBox()
        black_score_combo.addItems(point_system)
        black_score_combo.setFixedWidth(50)
        black_score_combo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        black_name_label = QLabel(black_name)

        row_layout.addWidget(white_name_label)
        row_layout.addWidget(white_score_combo)
        row_layout.addWidget(black_score_combo)
        row_layout.addWidget(black_name_label)

        self.main_window.pairings_scroll_layout.addLayout(row_layout)
        
        


        
    def pair_players(self,sim = False):
        round_listbox = self.main_window.round_listbox
        tournament_listbox = self.main_window.tournament_listbox
        tournament = self.main_window.get_current_tournament()
        round_players = tournament.players_in_current_round
        tournament_players = tournament.players
        point_system = tournament.point_system
        loss = point_system[0]
        draw = point_system[1]
        win = point_system[2]
        
        
        if ((not len(round_listbox) == 0 and len(self.main_window.pairings_scroll_layout) == 0)) or sim: # skip ui updates when sim is True
        
                            
            if tournament.rounds != tournament.current_round or tournament.rounds == 0: # can't pair more rounds than initalised, 0 bypasses this    
                # Reset half-byes and set has_played for this round
                for player in tournament_players:
                    player.add_half_bye_history(player.has_half_bye)
                    player.has_half_bye = False

                for player in round_players:
                    player.has_played = True

                # Players eligible for pairing (no recent half-bye)
                players_to_be_paired = []
                for player in round_players:
                    last_half_bye = player.half_bye_history[-1] if player.half_bye_history else False
                    if not last_half_bye:
                        players_to_be_paired.append(player)
                    else:
                        player.points_increment(draw) # planned bye gets a draw
                        player.add_point_history(draw)

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
                        lowest_scoring_player.points_increment(win) # win for odd numbered lowest scoring player
                        lowest_scoring_player.add_point_history(win)
                        
                        players_to_be_paired.remove(lowest_scoring_player)
                        print(f"{lowest_scoring_player.name} gets a bye this round.")
                    except ValueError:
                        # Handle the case when no player is eligible for a bye
                        print("No eligible player for a bye this round.")
                        lowest_scoring_player = None

                    
                
                # Create score buckets

                score_buckets = self.scoring_buckets(players_to_be_paired)
                all_players_flat = [p for b in score_buckets for p in b] # flatten bucket
                if not self.valid_pairings_exist(all_players_flat):# checks whether a valid pairing exists
                    print("No valid pairings possible this round!")
                    for player in tournament_players:
                        player.half_bye_history = player.half_bye_history[:-1] # reset the half bye history
                        
                        
                    return
                    
                valid_score_buckets = self.valid_buckets(score_buckets)

                            
                for bucket in valid_score_buckets:
                    if not self.valid_pairings_exist(bucket):  #flatten bucket if valid pairings do not exist
                        print("Error: No valid pairings in bucket after balancing flattening bucket!")            
                        valid_score_buckets = all_players_flat = [p for b in score_buckets for p in b] # flatten bucket
                        valid_score_buckets = [all_players_flat]

                        break
                    
                    
                # Generate final pairings
                tournament.pairings.clear() # clear the model first
                if tournament.current_round == 0: # first round paired differently
                    alternate_color = 0 # to alternate colors fairly in first round
                    for bucket in valid_score_buckets:
                        bucket_pairings = self.swiss_pairing(bucket) # pairings generated disregards color
                        for p1, p2 in bucket_pairings:
                            if alternate_color % 2 == 0:
                                if not sim:
                                    self.add_pairing_row(p1.name, p2.name)
                                p1.add_pairing("white",p2.id)
                                p2.add_pairing("black",p1.id)
                                tournament.add_pairing(p1,p2)
                            else:
                                if not sim:
                                    self.add_pairing_row(p2.name, p1.name)
                                p1.add_pairing("black",p2.id)
                                p2.add_pairing("white",p1.id)
                                tournament.add_pairing(p2,p1)
                            alternate_color+=1
                         
                else: # for every other round bar first
                    for bucket in valid_score_buckets: # highest scoring buckets paired first.
                        
                        sorted_bucket = sorted(bucket, key=lambda b: b.id)
                        bucket_pairings = self.swiss_pairing(sorted_bucket) # pairings generated disregards color
                     
                        for p1, p2 in bucket_pairings:
                            
                            p1_color_score = self.get_player_color_score(p1)
                            p2_color_score = self.get_player_color_score(p2)
                            #print("Color scores:", p1.name, p1_color_score, p2.name, p2_color_score)
                            
                            if p1_color_score < p2_color_score : # assign color later
                                if not sim:
                                    self.add_pairing_row(p1.name, p2.name)
                                    
                                
                                p1.add_pairing("white",p2.id)
                                p2.add_pairing("black",p1.id)
                                tournament.add_pairing(p1,p2)
                            elif p2_color_score < p1_color_score: 
                                if not sim:
                                    self.add_pairing_row(p2.name, p1.name)
                                p1.add_pairing("black",p2.id)
                                p2.add_pairing("white",p1.id)
                                tournament.add_pairing(p2,p1)
                            else: # color scores are equal, assign randomly
                                import random
                                if random.choice([True, False]):
                                    if not sim:
                                        self.add_pairing_row(p1.name, p2.name)
                                    p1.add_pairing("white",p2.id)
                                    p2.add_pairing("black",p1.id)
                                    tournament.add_pairing(p1,p2)
                                else:
                                    if not sim:
                                        self.add_pairing_row(p2.name, p1.name)
                                    p1.add_pairing("black",p2.id)
                                    p2.add_pairing("white",p1.id)
                                    tournament.add_pairing(p2,p1)
                        
                    
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
                if not sim:
                    tournament_listbox.clear()
                    for player in tournament.players:
                        self.main_window.player_controller.add_player_to_tournament_listbox(player)
                    self.main_window.tournament_tabs.setCurrentIndex(1)  # auto changes to second tab

            else:
                print("exceeded round limit")        
        else:
            print("emply round/ put score to players")

            
    def valid_buckets(self, score_buckets):
        """
        Balance score buckets by moving or merging.
        Flattening is the final fallback.
        """
        
        #print("total buckets before validation:", len(score_buckets))
        # Normalize buckets
        buckets = [list(b) for b in score_buckets if b] 
        
        # Base case
        if len(buckets) <= 1:
            return buckets
        
        # make sure each bucket has even number of players
        
        for i in range(len(buckets)):  # This loop ensures all buckets have even number of players
            if len(buckets[i]) % 2 == 1: # odd number of players in bucket
                
                float_player = buckets[i].pop()  # remove one player
                buckets[i + 1].append(float_player)  # add to next lower bucket
                
                return self.valid_buckets(buckets)  # recheck from start
        

        for i in range(len(buckets)): # if bucket has no valid pairings, try to merge it with next bucket
            
            valid_pairings = self.valid_pairings_exist(buckets[i])
            if valid_pairings: # if bucket has valid pairings check next bucket
                continue
            else:
                
                if i == len(buckets) - 1:  # last bucket, can't merge down so merge up
                    buckets[i - 1].extend(buckets[i])  # merge with next higher bucket
                    buckets[i] = []  # clear current bucket
                    
                
                else:   
                    buckets[i + 1].extend(buckets[i])  # merge with next lower bucket
                    buckets[i] = []  # clear current bucket
                #print("Merged bucket", i)
                return self.valid_buckets(buckets)
                
        return buckets
    
   
    def valid_pairings_exist(self, players): 
   
        if not players:
            return True

        player = players[0]

        for i in range(1, len(players)):
            opponent = players[i]
            if opponent.id in player.player_history:
                continue

            remaining = players[1:i] + players[i+1:]
            if self.valid_pairings_exist(remaining):
                return True

        return False


    def swiss_pairing(self, bucket_players): # pair the buckets
        """
        Swiss pairing with individual player swapping (floating)
        to ensure valid top-half vs bottom-half matchups.
        """
        # Sort by score descending
        players = sorted(bucket_players, key=lambda p: p.points, reverse=True)

        mid = len(players) // 2

        
       
        
         # normal can pair color not regarded
        def can_pair(top, bottom):
            """Backtracking test."""
            def backtrack(t, b, result):
                if not t:  # all top players paired
                    return result

                p = t[0]
                for i, opp in enumerate(b):
                    if opp.id in p.player_history:
                        continue  # skip invalid opponents
                    new_t = t[1:]
                    new_b = b[:i] + b[i+1:]
                    out = backtrack(new_t, new_b, result + [(p, opp)])
                    if out is not None:
                        return out  # found a complete pairing

                return None  # no valid opponent found, backtrack

            return backtrack(top, bottom, [])

        #print("Strict Swiss pairing failed — attempting player swaps...")
        
        # ----- First ATTEMPT: strict halves -----
        top = players[:mid] #try to pair top half vs bottom half
        bottom = players[mid:]

        result = can_pair(top, bottom)
        if result is not None:
            return result
       

        # ----- SWAP LOGIC (FLOATING) -----
        # Try swapping player from top with from bottom
        # try all combinations until a valid pairing is found 
        for i in range(len(top)):
            for j in range(len(bottom)):
                new_top = top.copy()
                new_bottom = bottom.copy()

                p_top = new_top.pop(i)
                p_bottom = new_bottom.pop(j)

                new_top.append(p_bottom) # switch players from top and bottom to enable pairings
                new_bottom.insert(0, p_top)

                result = can_pair(new_top, new_bottom)
                if result is not None:
                   # print(f"Swapped {p_top.name} with {p_bottom.name} to enable pairing.")
                    return result

    # ---- No valid pairing ----
        

        # If everything fails
        print("No valid Swiss pairings found even after swaps.")
        return []


    
    
    
    def get_player_color_score(self,player): # white is 1 black is -1, if color score is 2 they shoud be black next
        color_score = 0
        if player.color_history: # if color history exists
            for color in player.color_history:
                if color == "white":
                    color_score += 1
                elif color == "black":
                    color_score -= 1
            
            if color_score == 0:  # players should get paired alternating colors even if they have even number of black and white
                if player.color_history[-1] == "black": # if most recent game color is black
                    color_score -= 0.1 # slightly favour black
                elif player.color_history[-1] == "white":  # if most recent game color is white
                    color_score +=0.1 # slightly favour white
            return color_score
        return color_score
    
    def scoring_buckets(self, players_list): # puts players to be paired in their own scoring bucket
        
        buckets = [] # buckets to track unique scores
        unique_scores = [] # tracking unique scores
        for player in players_list:
            if player.points not in unique_scores:
                unique_scores.append(player.points) # put all unique scores in a list
                
        unique_scores.sort(reverse=True) # sort so first bucket is highest scoring bucket
        
        for _ in unique_scores:
            buckets.append([]) # create the buckets for scores
            
        for player in players_list:
            for i in range(len(unique_scores)):
                if unique_scores[i] == player.points:  # assign the player to the corresponding bucket score
                    buckets[i].append(player)
        #print(buckets)
        return buckets
            
            
            
            
            
        
        
        
        
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class PairPlayersController: # handle how tournament logic
    
    def __init__(self, main_window):
        self.main_window = main_window
        
    def add_pairing_row(self, white, black):
        tournament = self.main_window.get_current_tournament()
        point_system = tournament.point_system

        point_system = list(map(str, point_system)) # convert point system to string

        row_layout = QHBoxLayout()

        label1 = QLabel(white)

        combo1 = QComboBox()
        combo1.addItems(point_system)
        combo1.setFixedWidth(50)
        combo1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        combo2 = QComboBox()
        combo2.addItems(point_system)
        combo2.setFixedWidth(50)
        combo2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        label2 = QLabel(black)

        row_layout.addWidget(label1)
        row_layout.addWidget(combo1)
        row_layout.addWidget(combo2)
        row_layout.addWidget(label2)

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


            

                # Generate final pairings
                tournament.pairings.clear() # clear the model first
                if tournament.current_round == 0: # first round paired differently
                    alternate_color = 0
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
                    for bucket in reversed(valid_score_buckets): # reverse so highest scoring buckets paired first.
                        
                        sorted_bucket = sorted(bucket, key=lambda b: b.id)
                        bucket_pairings = self.swiss_pairing(sorted_bucket) # pairings generated disregards color
                     
                        for p1, p2 in bucket_pairings:
                            
                            p1_color_score = self.get_player_color_score(p1)
                            p2_color_score = self.get_player_color_score(p2)
                            #print(p1_color_score , p2_color_score)
                            if p1_color_score < p2_color_score : # assign color later
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

            # Odd bucket → move 1 player to next bucket
            if len(bucket) % 2 == 1:
                moved = False
                for i in range(len(bucket)):
                    player = bucket.pop(i)
                    score_buckets[b_index + 1].insert(0, player) # remove and put player to next bucket

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
                score_buckets[b_index + 1] = all_players + score_buckets[b_index + 1] # move all players down a bucket if no pairings exist
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
        
        # ----- Second ATTEMPT: strict halves -----
        top = players[:mid]
        bottom = players[mid:]

        result = can_pair(top, bottom)
        if result is not None:
            return result
       

        # ----- SWAP LOGIC (FLOATING) -----
        # Try swapping player from top with from bottom
        
        for i in range(mid):

            for j in range(mid): 
                player = top.pop(i)
                player2 = bottom.pop(j)
                
                bottom.insert(0,player)
                top.append(player2)
                
                

                result = can_pair(top, bottom)
                if result is not None:
                    print(f"Swapped {player.name} with {player2.name} to enable pairing.")
                    return result
        

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
                    color_score -= 0.1 
                elif player.color_history[-1] == "white":  # if most recent game color is white
                    color_score +=0.1
            return color_score
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
            
            
                
            
            
            
        
        
        
        
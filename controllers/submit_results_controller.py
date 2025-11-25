
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class SubmitResultsController: # submit scores and assigns scores
    
    def __init__(self, main_window):
        self.main_window = main_window
        
        
    def clear_layout(self,layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)

                # If the item is a widget, delete it
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()

                # If the item is a layout, clear it recursively
                else:
                    child_layout = item.layout()
                    if child_layout is not None:
                        self.clear_layout(child_layout)
                        
    def submit_results(self):
        
        
        
        row_layouts = self.get_rows_from_layout(self.main_window.pairings_scroll_layout)
        for row_widget in row_layouts:
            w = self.get_row_widgets(row_widget)

            label1 = w[0]      # QLabel White name
            combo1 = w[1]      # QComboBox white score
            combo2 = w[2]      # QComboBox Black score
            label2 = w[3]      # QLabel Black name

            print(label1.text(), combo1.currentText(), combo2.currentText(), label2.text())
            white_player = self.get_player_from_name(label1.text())
            black_player = self.get_player_from_name(label2.text())
            value_white = float(combo1.currentText())
            value_black = float(combo2.currentText())
            
            
            white_player.points_increment(value_white)
            white_player.add_point_history(value_white)
            black_player.points_increment(value_black)
            black_player.add_point_history(value_black)
            
            
            
        self.clear_layout(self.main_window.pairings_scroll_layout)
            
            
    
    
    def get_row_widgets(self,row_layout):
        widgets = []
        for i in range(row_layout.count()):
            w = row_layout.itemAt(i).widget()
            if w:
                widgets.append(w)
        return widgets
    
    def get_rows_from_layout(self, layout):
        row_layouts = []
        for i in range(layout.count()):
            item = layout.itemAt(i)

            if item.layout():
                row_layouts.append(item.layout())


        return row_layouts
    
    
    def random_scores(self): # assigns random scores to each player
        
        row_layouts = self.get_rows_from_layout(self.main_window.pairings_scroll_layout)        
        
        
        for row_widget in row_layouts:
            w = self.get_row_widgets(row_widget)

            combo1 = w[1]      # QComboBox white score            
            
            combo2 = w[2]      # QComboBox Black score
            
            import random

            if random.randint(1, 3) == 1: # 1/3 percent chance white wins
                
                combo1.setCurrentIndex(2)   # White wins
                combo2.setCurrentIndex(0)   # Black loses

            elif random.randint(1, 3) == 2: # 1/3 black wins
                combo1.setCurrentIndex(0)   # White loses
                combo2.setCurrentIndex(2)   # Black wins

            else: #1/3 it is a draw
                combo1.setCurrentIndex(1)   # White draws
                combo2.setCurrentIndex(1)   # Black draws
            
        
    def simulate_round_on_rating(self):
        row_layouts = self.get_rows_from_layout(self.main_window.pairings_scroll_layout)        

        
        for row_widget in row_layouts:
            w = self.get_row_widgets(row_widget)

            label1 = w[0]      # QLabel White name
            combo1 = w[1]      # QComboBox white score
            combo2 = w[2]      # QComboBox Black score
            label2 = w[3]      # QLabel Black name
            
            white_player = self.get_player_from_name(label1.text())
            black_player = self.get_player_from_name(label2.text())
            if abs(white_player.rating - black_player.rating) <= 50 : # makes draws less rare
                combo1.setCurrentIndex(1)   # White draws
                combo2.setCurrentIndex(1)   # Black draws
            elif white_player.rating < black_player.rating:
                combo1.setCurrentIndex(0)   # White loses
                combo2.setCurrentIndex(2)   # Black wins
            elif white_player.rating > black_player.rating :
                combo1.setCurrentIndex(2)   # White wins
                combo2.setCurrentIndex(0)   # Black loses
                
                
    def simulate_all_rounds(self):
        pass
                    
    def get_player_from_name(self,name):
        tournament = self.main_window.get_current_tournament()

        for player in tournament.players:
            if player.name == name:
                return player
        
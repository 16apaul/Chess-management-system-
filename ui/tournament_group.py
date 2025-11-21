from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def create_tournament_group(window): # create button group box to hold tournaments
         
        window.tournament_groupbox = QGroupBox("Tournaments", window) # Group box to hold tournament buttons
        window.layout.addWidget(window.tournament_groupbox, 0, 0)
        window.tournament_layout = QVBoxLayout()  
        window.tournament_layout.setAlignment(Qt.AlignTop)  # Align buttons to the top
        window.tournament_groupbox.setLayout(window.tournament_layout)
        
        # make the tournament buttons toggleable
        window.tournament_buttons = QButtonGroup(window)
        window.tournament_buttons.setExclusive(True)  # Only one button can be checked at a time
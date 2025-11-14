from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def create_tournament_tabs(window):
      #  tabs to the window layout


      window.tournament_tabs = QTabWidget() 
      window.layout.addWidget(window.tournament_tabs, 0, 1, 1, 3) # spans add to main layout spans three columns
      add_player_tab = QWidget()
      add_player_tab_layout = QGridLayout()
      add_player_tab.setLayout(add_player_tab_layout)



      window.tournament_listbox = QListWidget() #box to show list of players in tournament
      add_player_tab_layout.addWidget(window.tournament_listbox, 0, 0, 1,1)
      window.tournament_listbox.setSelectionMode(QListWidget.SingleSelection)



      window.add_player_lineedit = QLineEdit()
      window.add_player_lineedit.setPlaceholderText("Player name")
      add_player_tab_layout.addWidget(window.add_player_lineedit, 1, 0)
      window.add_player_rating_lineedit = QLineEdit()
      window.add_player_rating_lineedit.setPlaceholderText("Player rating")
      add_player_tab_layout.addWidget(window.add_player_rating_lineedit, 2, 0)
      add_player_button = QPushButton("Add Player") # button to add player to tournament
      add_player_tab_layout.addWidget(add_player_button, 3, 0,1,1)
      add_player_button.clicked.connect(window.player_controller.add_player_to_tournament) 



      add_all_players_to_round_button = QPushButton("Add all") # button to add all players to the current round
      add_player_tab_layout.addWidget(add_all_players_to_round_button, 1, 1,1,1)
      add_all_players_to_round_button.clicked.connect(window.round_controller.add_all_players_to_round)




      window.round_listbox = QListWidget() # box to show list of round players
      add_player_tab_layout.addWidget(window.round_listbox, 0, 2, 3,2)
      window.round_listbox.setSelectionMode(QListWidget.NoSelection) # allow multiple selection of players


      pair_button = QPushButton("Pair Round") # button to pair the current round
      add_player_tab_layout.addWidget(pair_button, 3, 2,1,2)
      pair_button.clicked.connect(window.pair_players)


      window.tournament_tabs.addTab(add_player_tab, "Add Players")






# pairings tab

      pairings_tab = QWidget()

      pairings_tab_layout = QGridLayout()
      pairings_tab.setLayout(pairings_tab_layout)


      window.pairings_scroll = QScrollArea()
      window.pairings_scroll.setWidgetResizable(True)

      # Create inner widget for scroll area
      window.pairings_content = QWidget()

      # Create layout on the content widget
      window.pairings_scroll_layout = QVBoxLayout(window.pairings_content)

      # Put the widget inside the scroll area
      window.pairings_scroll.setWidget(window.pairings_content)

      # Add scroll area to the tab layout
      pairings_tab_layout.addWidget(window.pairings_scroll, 0, 0, 5, 3)


      results_button = QPushButton("Submit results")
      pairings_tab_layout.addWidget(results_button, 0,3)
      results_button.clicked.connect(window.submit_results)





      window.tournament_tabs.addTab(pairings_tab, "Pairings")


      results_tab = QWidget()
      window.tournament_tabs.addTab(results_tab, "Results")
      window.tournament_tabs.hide()  # Hide tabs initially
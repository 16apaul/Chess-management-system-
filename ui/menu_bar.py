
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



def create_menu_bar(window):

        # Create a menu bar
        

        menubar = window.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        # actions for the File menu
        save_action = QAction("save", window)
        
        open_action = QAction("Open", window)
        
        
        exit_action = QAction("Exit", window)
        exit_action.triggered.connect(window.close)

        file_menu.addAction(save_action)
        
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        save_action.triggered.connect(window.persistence_controller.save_tournaments)
        open_action.triggered.connect(window.persistence_controller.load_all_tournaments)

        # Create Tournament menu
        tournament_menu = menubar.addMenu("Tournament") # add menu
        delete_tournament_action = QAction("Delete Tournament", window)
        tournament_menu.addAction(delete_tournament_action)

         # link menu to items
        create_tournament_action = QAction("Create Tournament", window) # create items for the menu

        menubar.addAction(create_tournament_action)

        

        import_dataset_action = QAction("Import Dataset", window)
        menubar.addAction(import_dataset_action)
        

        create_tournament_action.triggered.connect(window.tournament_controller.create_tournament) 
        delete_tournament_action.triggered.connect(window.tournament_controller.delete_tournament)
        import_dataset_action.triggered.connect(window.create_tournament_from_dataset)

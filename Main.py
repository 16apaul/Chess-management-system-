import sys
from tournament import Tournament
from player import Player
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction,QMessageBox,QPushButton,QInputDialog


tournaments = [] # List to hold tournament data
tournament_id = 1  # counter for tournament IDs  
player_id = 1 # counter for player IDs
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tournaments = {}  # Dictionary to hold tournament data

        self.setWindowTitle("Chess Manager")
        self.setGeometry(100, 100, 400, 300)

        # Create a menu bar
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        # Example actions
        new_action = QAction("save", self)
        open_action = QAction("Open", self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # Create Tournament menu
        create_tournament_menu = menubar.addMenu("create tournament") # add menu
        create_tournament_action = QAction("Create Tournament", self) # create items for the menu
        create_tournament_menu.addAction(create_tournament_action) # link menu to items
        self.button_y = 50  # Initial y position for create tournament buttons


        create_tournament_action.triggered.connect(self.create_tournament) 



    def create_tournament(self):
        print("Create Tournament action triggered")
        tournament_name, ok = QInputDialog.getText(
            self, "Tournament Name", "Enter tournament name:"
        )
        if ok and tournament_name:
            button = QPushButton(tournament_name, self)
            button.setGeometry(0,self.button_y,150,30)
            button.show()
            global tournament_id
            tournament = Tournament(tournament_id, tournament_name)
            tournaments.append(tournament)
            tournament_id += 1
            
            self.tournaments[tournament_name] = []
            button.clicked.connect(lambda checked, name=tournament_name: self.open_tournament(name))

            self.button_y += 40
        else:
            QMessageBox.warning(self, "Input Error", "Tournament name cannot be empty.")
        
    def open_tournament(self, name):
        # Add something to this tournament’s array
        self.tournaments[name].append("New player")
        data = self.tournaments[name]

        QMessageBox.information(
            self,
            "Tournament Data",
            f"Tournament: {name}\nData: {data}"
        )

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    
    p1 = Player(1,"Alice")
    t1 = Tournament(1,"Spring Open",[p1])
    print(t1)
    sys.exit(app.exec_())
    
    


        
        
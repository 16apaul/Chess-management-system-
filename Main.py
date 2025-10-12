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

        # actions for the File menu
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
        repeat_names = False
        for t in tournaments:
            if t.name == tournament_name:
                repeat_names = True
                break
        if ok and tournament_name and not repeat_names:
            button = QPushButton(tournament_name, self)
            button.setGeometry(0,self.button_y,100,30)
            button.show()
            global tournament_id
        
            tournament = Tournament(tournament_id, tournament_name)
            tournaments.append(tournament)
            
            self.tournaments[tournament_name] = [] #This creates a key in the dictionary
            button_id = tournament_id  # Capture the current tournament_id
            button.clicked.connect(lambda checked, name=tournament_name: self.open_tournament(name,button_id))
            tournament_id += 1


            self.button_y += 40
        else:
            QMessageBox.warning(self, "Input Error", "Tournament name cannot be empty and must be unique.")
        
    def open_tournament(self, name,id):
        # Add something to this tournament’s array
        print("hhh", tournaments, id)
        self.tournaments[name].append(tournaments[id-1]) # id-1 because id starts from 1 but list index starts from 0
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
    
    


        
        
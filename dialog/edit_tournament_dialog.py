from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class EditTournamentDialog(QDialog):
    def __init__(self, tournament, main_window):
        super().__init__()
        self.setWindowTitle("Edit Tournament")
        self.setFixedSize(320, 260)
        self.tournament = tournament  
        self.main_window = main_window
        main_layout = QVBoxLayout()
        grid = QGridLayout()

        #  Tournament Name
        name_label = QLabel("Tournament Name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Tournament Name")
        self.name_input.setText(tournament.name)

        # Disable editing if CSV
        if tournament.name.endswith(".csv"):
            self.name_input.setEnabled(False)

        # Point System
        point_system = tournament.point_system #[0,0.5,1] is default
        
        win_label = QLabel("Points for Win:")
        self.win_input = QLineEdit()
        self.win_input.setPlaceholderText("e.g. 1")
        self.win_input.setText(str(point_system[2]))

        draw_label = QLabel("Points for Draw:")
        self.draw_input = QLineEdit()
        self.draw_input.setPlaceholderText("e.g. 0.5")
        self.draw_input.setText(str(point_system[1]))

        loss_label = QLabel("Points for Loss:")
        self.loss_input = QLineEdit()
        self.loss_input.setPlaceholderText("e.g. 0")
        self.loss_input.setText(str(point_system[0]))

        
        # Rounds Input
        rounds_label = QLabel("Number of Rounds:")
        self.rounds_input = QLineEdit()
        self.rounds_input.setPlaceholderText("e.g. 5")
        self.rounds_input.setText(str(tournament.rounds))
        
        # tournament type
        self.tournament_type_label = QLabel("Current tournament type:")
        self.tournament_type_combo = QComboBox()
        self.tournament_type_combo.addItems(["Swiss", "Double Round Robin", "Knockout"])
        self.tournament_type_combo.setCurrentText(tournament.style)
        
        # Disable points and rounds and type editing after tournament starts
        if tournament.current_round == 0:
            self.win_input.setEnabled(True)
            self.draw_input.setEnabled(True)
            self.loss_input.setEnabled(True)
            
            self.rounds_input.setEnabled(True)
            
            self.tournament_type_combo.setEnabled(True)


        else:
            self.win_input.setEnabled(False)
            self.draw_input.setEnabled(False)
            self.loss_input.setEnabled(False)
            
            self.rounds_input.setEnabled(False)
            
            self.tournament_type_combo.setEnabled(False)

            
        # tournament data inputs
        self.date_label = QLabel("Tournament Date:")
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)  # shows calendar
        if tournament.date:
            date_parts = tournament.date.split("/")  # assuming format "dd/MM/yyyy"
            day = int(date_parts[0])
            month = int(date_parts[1])
            year = int(date_parts[2])
            self.date_input.setDate(QDate(year, month, day))
        else:
            self.date_input.setDate(QDate.currentDate()) # set to current date of tournament
        self.date_input.setDisplayFormat("dd/MM/yyyy")
        

        
        
            
        
        
        
        # Grid Layout Placement
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_input, 0, 1)

        grid.addWidget(win_label, 1, 0)
        grid.addWidget(self.win_input, 1, 1)

        grid.addWidget(draw_label, 2, 0)
        grid.addWidget(self.draw_input, 2, 1)

        grid.addWidget(loss_label, 3, 0)
        grid.addWidget(self.loss_input, 3, 1)

        grid.addWidget(rounds_label, 4, 0)
        grid.addWidget(self.rounds_input, 4, 1)
        
        grid.addWidget(self.tournament_type_label, 5,0)
        grid.addWidget(self.tournament_type_combo, 5,1)
        
        grid.addWidget(self.date_label, 6,0)
        grid.addWidget(self.date_input, 6,1)
        
        # Save Button
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_changes)

        # Final Layout
        main_layout.addLayout(grid)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.save_btn)

        self.setLayout(main_layout)

    def save_changes(self): 
        

        #get values of tournament dict from main window
        tournaments = self.main_window.tournaments  # dict {name: Tournament}
        
        new_name = self.name_input.text().strip()
        if new_name == "":
            QMessageBox.warning(self, "Invalid Name", "Tournament name cannot be empty.")
            return
        # Check for duplicate names
        for existing_name, t in tournaments.items():
            if t is not self.tournament and existing_name == new_name:
                QMessageBox.warning(
                    self,
                    "Duplicate Name",
                    "A tournament with this name already exists."
                )
                return
            
        self.tournament.name = new_name
        self.tournament.style = self.tournament_type_combo.currentText()
        self.tournament.date = self.date_input.date().toString("dd/MM/yyyy")
        
         # Try to update point system and rounds
         # Show error message if invalid
         # Close dialog if successful
         # Update tournament object
        try:
            self.tournament.point_system = [
                float(self.loss_input.text()),
                float(self.draw_input.text()),
                float(self.win_input.text())
            ]
            self.tournament.rounds = int(self.rounds_input.text())

            
            

            self.accept()   # Close 

        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Points/rounds must be numbers!")

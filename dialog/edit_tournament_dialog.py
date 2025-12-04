from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton,
    QMessageBox, QGridLayout, QLabel
)

class EditTournamentDialog(QDialog):
    def __init__(self, tournament):
        super().__init__()
        self.setWindowTitle("Edit Tournament")
        self.setFixedSize(320, 260)
        self.tournament = tournament  

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

        # Disable points editing after tournament starts
        if tournament.current_round == 0:
            self.win_input.setEnabled(True)
            self.draw_input.setEnabled(True)
            self.loss_input.setEnabled(True)
        else:
            self.win_input.setEnabled(False)
            self.draw_input.setEnabled(False)
            self.loss_input.setEnabled(False)

        # Grid Layout Placement
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_input, 0, 1)

        grid.addWidget(win_label, 1, 0)
        grid.addWidget(self.win_input, 1, 1)

        grid.addWidget(draw_label, 2, 0)
        grid.addWidget(self.draw_input, 2, 1)

        grid.addWidget(loss_label, 3, 0)
        grid.addWidget(self.loss_input, 3, 1)

        # Save Button
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_changes)

        # Final Layout
        main_layout.addLayout(grid)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.save_btn)

        self.setLayout(main_layout)

    def save_changes(self):
        try:
            self.tournament.name = self.name_input.text()

            self.tournament.point_system = [
                float(self.loss_input.text()),
                float(self.draw_input.text()),
                float(self.win_input.text())
            ]

            self.accept()   # Close 

        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Points must be numbers!")

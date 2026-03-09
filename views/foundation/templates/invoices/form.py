from PySide6.QtWidgets import (
     QWidget, QLabel, QLineEdit, QGridLayout
)

class FormTemplate(QWidget):
    def __init__(self):
        super().__init__()

        # Labels et inputs
        self.company_name_label = QLabel("Raison sociale:")
        self.company_name_input = QLineEdit()

        self.responsable_label = QLabel("Responsable:")
        self.responsable_input = QLineEdit()

        self.stat_label = QLabel("Statistic:")
        self.stat_input = QLineEdit()

        self.nif_label = QLabel("NIF:")
        self.nif_input = QLineEdit()

        # Layout en grille (2 colonnes)
        layout = QGridLayout()

        layout.setVerticalSpacing(0)

        # Colonne 0 : Raison sociale + Statistic
        layout.addWidget(self.company_name_label, 0, 0)
        layout.addWidget(self.company_name_input, 1, 0)

        layout.addWidget(self.stat_label, 2, 0)
        layout.addWidget(self.stat_input, 3, 0)

        # Colonne 1 : Responsable + NIF
        layout.addWidget(self.responsable_label, 0, 1)
        layout.addWidget(self.responsable_input, 1, 1)

        layout.addWidget(self.nif_label, 2, 1)
        layout.addWidget(self.nif_input, 3, 1)

        self.setLayout(layout)
        self.setWindowTitle("Formulaire")

        # Charger le style depuis input.qss
        with open("styles/input.qss", "r") as f:
            style = f.read()
            self.setStyleSheet(style)


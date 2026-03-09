from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QFormLayout, QHBoxLayout
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

        # Layout principal horizontal (2 colonnes)
        main_layout = QHBoxLayout()

        # Colonne gauche
        left_form = QFormLayout()
        left_form.setSpacing(0)
        left_form.addRow(self.company_name_label, self.company_name_input)
        left_form.addRow(self.stat_label, self.stat_input)

        # Colonne droite
        right_form = QFormLayout()
        right_form.setSpacing(0)
        right_form.addRow(self.responsable_label, self.responsable_input)
        right_form.addRow(self.nif_label, self.nif_input)

        # Ajouter les deux colonnes côte à côte
        main_layout.addLayout(left_form)
        main_layout.addLayout(right_form)

        self.setLayout(main_layout)
        self.setWindowTitle("Formulaire")

        # Charger le style depuis input.qss
        with open("styles/input.qss", "r") as f:
            style = f.read()
            self.setStyleSheet(style)


from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QVBoxLayout, QLineEdit, QLabel, QWidget, QHBoxLayout, QPushButton
from PySide6 import QtCore

class ListRecordTemplate(QWidget):

    def __init__(self, headers : list[str], data: list = None, parent=None):
        super().__init__(parent)
        self.headers = headers
        self.data = data or []
        self.all_data = self.data.copy()  # Keep original data for filtering
        
        layout = QVBoxLayout(self)
        
        # Search box and delete button
        search_layout = QHBoxLayout()
        self.search_label = QLabel("Rechercher:")
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.filter_data)
        self.delete_button = QPushButton("Supprimer")
        self.delete_button.setObjectName("deleteRecordButton")
        self.delete_button.clicked.connect(self.delete_selected_record)
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_input, 1)  # Take remaining space
        search_layout.addWidget(self.delete_button, 1)  # Take 1/2 of the space
        layout.addLayout(search_layout)
        
        # Table
        self.table = QTableWidget()
        self._setup_table()
        self._add_row()
        self.table.itemSelectionChanged.connect(self.on_item_selected)
        layout.addWidget(self.table)

    def _setup_table(self):
        # Nombre de colonnes dynamique
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSortingEnabled(True)  # Enable sorting
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)

    def _add_row(self):
        self.table.setRowCount(0)
        data_to_show = self.data if self.data else self.all_data
        if not data_to_show:
            self.table.setRowCount(1)
            item = QTableWidgetItem("Aucun donné disponible dans toute la table")
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table.setItem(0, 0, item)
            self.table.setSpan(0, 0, 1, len(self.headers))
            return
        for row_data in data_to_show:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for column, value in enumerate(row_data):
                self.table.setItem(row_position, column, QTableWidgetItem(str(value)))

    def on_item_selected(self):
        current_row = self.table.currentRow()
        if current_row >= 0 and hasattr(self.parent(), 'load_invoice_data'):
            invoice_id = self.table.item(current_row, 0).text()
            self.parent().load_invoice_data(invoice_id)

    def filter_data(self):
        search_text = self.search_input.text().lower()
        if not search_text:
            self.data = self.all_data.copy()
        else:
            self.data = [row for row in self.all_data if any(search_text in str(cell).lower() for cell in row)]
        self._add_row()

    def delete_selected_record(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            invoice_id = self.table.item(current_row, 0).text()
            if hasattr(self.parent(), 'delete_invoice'):
                self.parent().delete_invoice(invoice_id)

    def update_data(self, new_data):
        self.all_data = new_data.copy()
        self.data = self.all_data.copy()
        self.search_input.clear()
        self._add_row()
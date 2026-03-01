from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView


class ListRecordTemplate(QTableWidget):
    def __init__(self, headers: list[str], parent=None):
        super().__init__(parent)

        self.headers = headers
        self._setup_table()
        
    # def _setup_table(self):
    #     # Nombre de colonnes dynamique
    #     self.setColumnCount(len(self.headers))
    #     self.setHorizontalHeaderLabels(self.headers)
    #     self.setSelectionBehavior(self.SelectRows)
    #     self.setEditTriggers(self.NoEditTriggers)
    #     self.horizontalHeader().setStretchLastSection(True)
    #     self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # def add_row(self, data: list):
    #     row_position = self.rowCount()
    #     self.insertRow(row_position)

    #     for column, value in enumerate(data):
    #         self.setItem(row_position, column, QTableWidgetItem(str(value)))
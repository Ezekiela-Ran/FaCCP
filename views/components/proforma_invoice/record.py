from PySide6.QtWidgets import QWidget
from PySide6.QtCore import (Qt)

class ProformaInvoiceRecord(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
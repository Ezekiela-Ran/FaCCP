from PySide6 import QtWidgets,QtCore
class StandardInvoiceRecord(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("card")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        
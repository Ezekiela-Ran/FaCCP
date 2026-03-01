from views.foundation.templates.invoices.form import FormTemplate
from PySide6 import QtWidgets,QtCore
class StandardInvoiceForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        std_layout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("card")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
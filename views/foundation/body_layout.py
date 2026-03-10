from PySide6 import QtWidgets,QtCore
from views.components.standard_invoice.product_type import StandardInvoiceProductType
from views.components.standard_invoice.products import StandardInvoiceProducts

class BodyLayout(QtWidgets.QWidget):
    def __init__(self,parent):
        super().__init__(parent)

        self.setObjectName("card")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)   

        self.body_layout = QtWidgets.QVBoxLayout(self)
        

        self.form = StandardInvoiceProductType()
        self.form.setMaximumWidth(300)
        self.record = StandardInvoiceProducts()

        self.body_layout.addWidget(self.form, 1)
        self.body_layout.addWidget(self.record, 1)
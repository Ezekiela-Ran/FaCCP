from views.foundation.templates.products import ProductsTemplate
from PySide6 import QtWidgets,QtCore
class StandardInvoiceProducts(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("productType")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.products_template = ProductsTemplate()
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.products_template)
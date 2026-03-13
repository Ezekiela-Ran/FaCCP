from views.foundation.templates.product_type import ProductTypeTemplate
from PySide6 import QtWidgets
class StandardInvoiceProductType(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.product_type_template = ProductTypeTemplate()
        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(self.product_type_template)

        
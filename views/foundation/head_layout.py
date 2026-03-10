from PySide6 import QtWidgets
from views.components.standard_invoice.form import StandardInvoiceForm
from views.components.proforma_invoice.form import ProformaInvoiceForm
from views.components.standard_invoice.record import StandardInvoiceRecord
from views.components.proforma_invoice.record import ProformaInvoiceRecord


class HeadLayout(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.head_layout = QtWidgets.QHBoxLayout(self)
        self.head_layout.setContentsMargins(0, 0, 0, 0)

    def standard_invoice(self):
        self.form = StandardInvoiceForm()
        self.record = StandardInvoiceRecord()

        self.head_layout.addWidget(self.form, 1)
        self.head_layout.addWidget(self.record, 1)

    def proforma_invoice(self):
        self.form = ProformaInvoiceForm()
        self.record = ProformaInvoiceRecord()

        self.head_layout.addWidget(self.form, 1)
        self.head_layout.addWidget(self.record, 1)
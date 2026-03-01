from PySide6 import QtWidgets
from views.components.invoices.form.standard import StandardInvoiceForm
from views.components.invoices.records.standard import StandardInvoiceRecord
from views.foundation.templates.invoices.form import FormTemplate

class HeadLayout(QtWidgets.QWidget):
    def __init__(self,parent):
        super().__init__(parent)
        
        self.head = QtWidgets.QHBoxLayout(self)
        
        self.form = StandardInvoiceForm()
        self.record = StandardInvoiceRecord()

        # Facteur d’étirement
        self.head.addWidget(self.form,3)
        self.head.addWidget(self.record,2)
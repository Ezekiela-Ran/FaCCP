from views.foundation.templates.form import FormTemplate
from PySide6.QtCore import (Qt)
from PySide6.QtWidgets import (QLabel, QLineEdit, QDateEdit)

class ProformaInvoiceForm(FormTemplate):
    def __init__(self):
        super().__init__()
        self.setObjectName("card")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.date_label = QLabel("Date:")
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)

    
        self.proforma_invoice_number_label = QLabel("N° Facture proforma")
        self.proforma_invoice_number = QLineEdit()
        self.proforma_invoice_number.setFixedWidth(0)

        self.right_form.addRow(self.date_label, self.date_input)
        self.left_form.addRow(self.proforma_invoice_number_label, self.proforma_invoice_number)
from views.foundation.templates.invoices.form import FormTemplate
from PySide6.QtCore import (Qt)
from PySide6.QtWidgets import (QLabel, QLineEdit)


class StandardInvoiceForm(FormTemplate):
    def __init__(self):
        super().__init__()
        self.setObjectName("card")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # Labels et inputs
        self.product_ref_label = QLabel("Ref produit:")
        self.product_ref_input = QLineEdit()

        self.date_issue_label = QLabel("Date d'émission:")
        self.date_issue_input = QLineEdit()

        self.date_result_label = QLabel("Date de résultat:")
        self.date_result_input = QLineEdit()

        self.standard_invoice_number = QLabel("N° facture:")
        
        # Colonne gauche
        self.left_form.addRow(self.date_issue_label, self.date_issue_input)
        self.left_form.addRow(self.standard_invoice_number)

        # Colonne droite
        self.right_form.addRow(self.date_result_label, self.date_result_input)
        self.right_form.addRow(self.product_ref_label, self.product_ref_input)
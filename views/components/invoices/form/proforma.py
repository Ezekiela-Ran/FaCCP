from views.foundation.templates.invoices.form import FormTemplate
from PySide6.QtCore import (Qt)

class ProformaInvoiceForm(FormTemplate):
    def __init__(self):
        super().__init__()
        self.setObjectName("card")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
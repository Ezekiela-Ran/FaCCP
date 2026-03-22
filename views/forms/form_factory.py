from views.components.standard_invoice.form import StandardInvoiceForm
from views.components.proforma_invoice.form import ProformaInvoiceForm

class FormFactory:
    @staticmethod
    def create_standard_form():
        return StandardInvoiceForm()

    @staticmethod
    def create_proforma_form():
        return ProformaInvoiceForm()
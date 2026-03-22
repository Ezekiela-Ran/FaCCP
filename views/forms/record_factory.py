from views.components.standard_invoice.record import StandardInvoiceRecord
from views.components.proforma_invoice.record import ProformaInvoiceRecord

class RecordFactory:
    @staticmethod
    def create_standard_record():
        return StandardInvoiceRecord()

    @staticmethod
    def create_proforma_record():
        return ProformaInvoiceRecord()
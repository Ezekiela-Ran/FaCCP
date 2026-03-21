from models.database_manager import DatabaseManager

class ProformaInvoice(DatabaseManager):
    table_name = "proform_invoice"
    headers = ["N° de la facture proforma", "Raison sociale","Date","Responsable"]
    data = []
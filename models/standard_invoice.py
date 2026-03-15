from models.invoices_model import InvoicesModel

class StandardInvoice(InvoicesModel):
    table_name = "standard_invoice"
    headers = ["Raison sociale","Adresse","Date d'émission","Date de resultat","réference produit","Responsable"]
    data = []
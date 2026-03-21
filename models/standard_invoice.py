from models.database_manager import DatabaseManager

class StandardInvoice(DatabaseManager):
    table_name = "standard_invoice"
    headers = ["Raison sociale","Adresse","Date d'émission","Date de resultat","réference produit","Responsable"]
    data = []
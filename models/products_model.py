from models.database_manager import DatabaseManager

class ProductsModel(DatabaseManager):
    table_name = "products"
    name_column = "product_name"
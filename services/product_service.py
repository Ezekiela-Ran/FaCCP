from models.database_manager import DatabaseManager

class ProductService:
    def __init__(self):
        self.db = DatabaseManager()

    def get_products_by_type(self, type_id):
        return self.db.get_products_by_type(type_id)

    def get_product_by_id(self, product_id):
        return self.db.get_product_by_id(product_id)

    def add_product(self, type_id, name):
        return self.db.add_product(type_id, name)

    def update_product(self, pid, ref, num_act, physico, toxico, micro, subtotal):
        return self.db.update_product(pid, ref, num_act, physico, toxico, micro, subtotal)

    def delete_product(self, pid):
        return self.db.delete_product(pid)

    def insert_type(self, name):
        return self.db.insert_type(name)

    def delete_type(self, tid):
        return self.db.delete_type(tid)
from models.database.tables import Tables

class DatabaseManager(Tables):
    table_name = ""

    @classmethod
    def create_tables(cls):
        db = cls()
        try:
            db.proforma_invoice_table()
            db.standard_invoice_table()
            db.product_type_table()
            db.products_table()
        finally:
            db.close()

    def fetch_all(self):
        cursor = self.conn.cursor(dictionary=True)
        try:
            cursor.execute(f"SELECT * FROM {self.table_name}")
            return cursor.fetchall()
        finally:
            cursor.close()

    def insert_type(self, name: str):
        cursor = self.conn.cursor()
        try:
            query = "INSERT INTO product_type (product_type_name) VALUES (%s)"
            cursor.execute(query, (name,))
            self.conn.commit()
        finally:
            cursor.close()

    def delete_type(self, type_id: int):
        cursor = self.conn.cursor()
        try:
            query = "DELETE FROM product_type WHERE id = %s"
            cursor.execute(query, (type_id,))
            self.conn.commit()
        finally:
            cursor.close()


    def update(self, data, where):
        cursor = self.conn.cursor()
        try:
            set_clause = ", ".join([f"{col} = %s" for col in data.keys()])
            conditions = " AND ".join([f"{col} = %s" for col in where.keys()])
            query = f"UPDATE {self.table_name} SET {set_clause} WHERE {conditions}"
            values = list(data.values()) + list(where.values())
            cursor.execute(query, values)
            self.conn.commit()
        finally:
            cursor.close()

from models.database.connection import connection
def create_table():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS invoicing")
    cursor.execute("USE invoicing")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS proforma_invoice (
        id INT AUTO_INCREMENT PRIMARY KEY,
        company_name VARCHAR(255) NOT NULL,
        nif VARCHAR(255),
        stat VARCHAR(255),
        date DATE NOT NULL,
        resp VARCHAR(255) NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS standard_invoice (
        id INT AUTO_INCREMENT PRIMARY KEY,
        company_name VARCHAR(255) NOT NULL,
        stat VARCHAR(255),
        nif VARCHAR(255),
        adress VARCHAR(255),
        date_issue DATE NOT NULL,
        date_result DATE NOT NULL,
        product_ref VARCHAR(255) NOT NULL,
        resp VARCHAR(255) NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product_type (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_type_name VARCHAR(255) NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_name VARCHAR(255) NOT NULL,
        ref_b_analyse INT NOT NULL,
        num_act VARCHAR(255),
        physico INT,
        micro INT,
        toxico INT,
        sum INT,
        product_type_id INT NOT NULL,
        FOREIGN KEY (product_type_id)
        REFERENCES product_type(id)
        ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()
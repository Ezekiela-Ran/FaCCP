from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QTableWidget, QAbstractItemView, QLineEdit, QLabel, QInputDialog
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class ProductManager(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        
        self.db = db_manager

        # cadre principale
        main_layout = QHBoxLayout()

        # Types
        type_list_layout = QVBoxLayout()
        main_layout.addLayout(type_list_layout, 1)

        self.label= QLabel("Catégorie")
        self.add_type_btn = QPushButton("Ajouter")
        self.del_type_btn = QPushButton("Supprimer")
        self.type_list = QListWidget()

        type_list_layout.addWidget(self.label)
        type_list_layout.addWidget(self.add_type_btn)
        type_list_layout.addWidget(self.del_type_btn)
        type_list_layout.addWidget(self.type_list)
        
        # Produits
        product_list_layout = QVBoxLayout()
        main_layout.addLayout(product_list_layout, 3)

        self.add_product_btn = QPushButton("Ajouter")
        self.del_product_btn = QPushButton("Supprimer")
        self.save_btn = QPushButton("Enregistrer")

        self.product_table = QTableWidget()
        self.product_table.setColumnCount(10)
        self.product_table.setHorizontalHeaderLabels(["Désignation", "Ref.b.analyse", "N°Acte", "Physico", "Toxico", "Micro", "Sous total", "Suppr", "Modif", "Select"])
        self.product_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        product_list_layout.addWidget(self.add_product_btn)
        product_list_layout.addWidget(self.del_product_btn)
        product_list_layout.addWidget(self.product_table)
        product_list_layout.addWidget(self.save_btn)

        self.setLayout(main_layout)

        # Connexions
        self.add_type_btn.clicked.connect(self.add_type)
        self.del_type_btn.clicked.connect(self.del_type)
        self.add_product_btn.clicked.connect(self.add_product)
        self.del_product_btn.clicked.connect(self.del_product)
        self.save_btn.clicked.connect(self.save_products)
        self.type_list.itemSelectionChanged.connect(self.load_products)

        self.load_types()
    
    def load_types(self):
        self.type_list.clear()
        self.db.table_name = "product_type"
        for row in self.db.fetch_all():
            name = row["product_type_name"]
            self.type_list.addItem(name)


    def add_type(self):
        self.db.table_name = "product_type"
        name, ok = QInputDialog.getText(self, "Nouveau Type", "Nom du type:")
        if ok and name:
            self.db.insert_type(name)
            self.load_types()

    def del_type(self):
        if not self.type_list.currentItem():
            return
        tid = int(self.type_list.currentItem().text().split(" - ")[0])
        self.db.delete_type(tid)
        self.load_types()
        self.product_table.setRowCount(0)

    def add_product(self):
        if not self.type_list.currentItem():
            return
        tid = int(self.type_list.currentItem().text().split(" - ")[0])
        name, ok = QInputDialog.getText(self, "Nouveau Produit", "Nom du produit:")
        if ok and name:
            pid = self.db.add_product(tid, name)
            self.add_product_row(pid, name, "0", "0", "0")

    def del_product(self):
        if self.product_table.currentRow() >= 0:
            self.product_table.removeRow(self.product_table.currentRow())

    def save_products(self):
        # Envoyer uniquement les produits sélectionnés
        selected_ids = [pid for pid, sel in self.selected_products.items() if sel]
        print("Produits sélectionnés à enregistrer:", selected_ids)
        # Faire un INSERT dans une table de commandes ou autre logique

    def load_products(self):
        pass
        # self.product_table.setRowCount(0)
        # if not self.type_list.currentItem():
        #     return
        # tid = int(self.type_list.currentItem().text().split(" - ")[0])
        # for pid, name, ref, qual, price in self.db.get_products_by_type(tid):
        #     self.add_product_row(pid, name, ref, qual, price)


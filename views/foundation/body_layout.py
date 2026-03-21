from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from views.components.standard_invoice.product_manager import ProductManager
from models.database_manager import DatabaseManager

class BodyLayout(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout principal
        self.body_layout = QtWidgets.QHBoxLayout(self)
        self.body_layout.setContentsMargins(0, 0, 0, 0)

        self.setObjectName("card")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        db_manager = DatabaseManager()
        # Gestion des produits:
        self.product_manager = ProductManager(db_manager)
        self.product_manager.setObjectName("productType")
        self.product_manager.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.body_layout.addWidget(self.product_manager)

        # Chargement du style QSS
        self._apply_stylesheet("styles/product_type.qss")


    def _apply_stylesheet(self, path: str):
        """Charge et applique une feuille de style QSS depuis un fichier."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Fichier de style introuvable : {path}")


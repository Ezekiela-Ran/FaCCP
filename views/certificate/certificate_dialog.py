"""
Popup de sélection des types de certificat (CC / CNC) par produit sélectionné.
Chaque produit est soit CC (Consommable) soit CNC (Non Consommable), pas les deux.
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QCheckBox, QWidget, QAbstractItemView, QLabel, QHeaderView,
    QMessageBox,
)
from PySide6.QtCore import Qt

from views.certificate.certificate_printer import CertificatePrinter


class CertificateDialog(QDialog):
    """
    Dialogue de sélection CC / CNC.

    Paramètres
    ----------
    parent      : widget parent (body_layout)
    form        : formulaire client actif (StandardInvoiceForm / ProformaInvoiceForm)
    selected_products : liste ordonnée de product_id sélectionnés
    db_manager  : DatabaseManager pour résoudre les noms de produits
    """

    def __init__(self, parent, form, selected_products, db_manager):
        super().__init__(parent)
        self.form = form
        self.selected_products = selected_products
        self.db_manager = db_manager
        # rows: list of (pid, product_name, cc_checkbox, cnc_checkbox)
        self._rows: list[tuple] = []

        self.setWindowTitle("Certificats — CC / CNC")
        self.setMinimumSize(620, 380)
        self.setModal(True)

        self._build_ui()
        self._load_products()

    # ------------------------------------------------------------------
    # Construction de l'interface
    # ------------------------------------------------------------------

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(14, 14, 14, 14)

        title = QLabel("Sélectionner le type de certificat pour chaque produit")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 13px; margin-bottom: 4px;")
        layout.addWidget(title)

        self._table = QTableWidget()
        self._table.setColumnCount(3)
        self._table.setHorizontalHeaderLabels([
            "Désignation",
            "CC  (Certificat de Consommabilité)",
            "CNC  (Cert. de Non Consommabilité)",
        ])
        self._table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._table.setSelectionMode(QAbstractItemView.NoSelection)
        self._table.setAlternatingRowColors(True)
        self._table.verticalHeader().setVisible(False)
        hdr = self._table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.Stretch)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        layout.addWidget(self._table)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self._print_btn = QPushButton("Imprimer")
        self._print_btn.setObjectName("certificatePrintButton")
        self._print_btn.setMinimumWidth(110)
        self._print_btn.clicked.connect(self._on_print_clicked)
        btn_row.addWidget(self._print_btn)
        layout.addLayout(btn_row)

    def _load_products(self):
        self._table.setRowCount(len(self.selected_products))
        for i, pid in enumerate(self.selected_products):
            product = self.db_manager.get_product_by_id(pid)
            name = product["product_name"] if product else f"Produit {pid}"
            self._add_row(i, pid, name)

    def _add_row(self, row_index: int, pid, name: str):
        """Ajoute une ligne au tableau avec les deux cases à cocher mutuellement exclusives."""
        item = QTableWidgetItem(name)
        item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self._table.setItem(row_index, 0, item)

        cc_cb = self._make_centered_checkbox()
        cnc_cb = self._make_centered_checkbox()

        self._table.setCellWidget(row_index, 1, cc_cb)
        self._table.setCellWidget(row_index, 2, cnc_cb)

        # Exclusion mutuelle
        actual_cc = cc_cb.findChild(QCheckBox)
        actual_cnc = cnc_cb.findChild(QCheckBox)
        _wire_exclusive(actual_cc, actual_cnc)

        self._rows.append((pid, name, actual_cc, actual_cnc))

    @staticmethod
    def _make_centered_checkbox() -> QWidget:
        """Retourne un QWidget contenant un QCheckBox centré."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(QCheckBox())
        return container

    # ------------------------------------------------------------------
    # Logique
    # ------------------------------------------------------------------

    def _get_assignments(self) -> list[tuple]:
        """
        Retourne la liste des certificats à imprimer.
        Chaque élément : (pid, product_name, cert_type)
        cert_type vaut 'CC', 'CNC', ou None si pas coché.
        """
        result = []
        for pid, name, cc_cb, cnc_cb in self._rows:
            if cc_cb.isChecked():
                cert_type = "CC"
            elif cnc_cb.isChecked():
                cert_type = "CNC"
            else:
                cert_type = None
            result.append((pid, name, cert_type))
        return result

    def _on_print_clicked(self):
        assignments = self._get_assignments()
        to_print = [(pid, name, ct) for pid, name, ct in assignments if ct is not None]

        if not to_print:
            QMessageBox.warning(
                self,
                "Aucun certificat",
                "Veuillez sélectionner CC ou CNC pour au moins un produit.",
            )
            return

        printer = CertificatePrinter(self)
        printer.print_certificates(self.form, to_print)


# ------------------------------------------------------------------
# Utilitaire
# ------------------------------------------------------------------

def _wire_exclusive(cb_a: QCheckBox, cb_b: QCheckBox):
    """Rend cb_a et cb_b mutuellement exclusifs sans utiliser QButtonGroup."""

    def on_a(checked, _b=cb_b):
        if checked:
            _b.blockSignals(True)
            _b.setChecked(False)
            _b.blockSignals(False)

    def on_b(checked, _a=cb_a):
        if checked:
            _a.blockSignals(True)
            _a.setChecked(False)
            _a.blockSignals(False)

    cb_a.toggled.connect(on_a)
    cb_b.toggled.connect(on_b)

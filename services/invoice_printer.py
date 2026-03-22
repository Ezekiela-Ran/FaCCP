from PySide6 import QtWidgets
from PySide6.QtCore import QMarginsF
from PySide6.QtGui import QTextDocument, QPageSize, QPageLayout
from PySide6.QtWidgets import QMessageBox
from PySide6.QtPrintSupport import QPrinter, QPrintPreviewDialog


class InvoicePrinter:
    def __init__(self, parent_widget):
        self.parent = parent_widget

    def _load_print_css(self):
        try:
            with open("styles/invoice_print.css", "r", encoding="utf-8") as css_file:
                return css_file.read()
        except FileNotFoundError:
            return ""

    def generate_invoice_html(self, form, invoice_type, selected_products, db_manager):
        company_name = form.company_name_input.text().strip()
        responsable = form.responsable_input.text().strip()
        stat = form.stat_input.text().strip()
        nif = form.nif_input.text().strip()
        address = form.address_input.text().strip() if hasattr(form, 'address_input') else ""

        date_issue = ''
        date_result = ''
        date = ''

        if invoice_type == 'standard':
            date_issue = form.date_issue_input.date().toString('yyyy-MM-dd') if hasattr(form, 'date_issue_input') else ''
            date_result = form.date_result_input.date().toString('yyyy-MM-dd') if hasattr(form, 'date_result_input') else ''
            title = 'FACTURE'
        else:
            date = form.date_input.date().toString('yyyy-MM-dd') if hasattr(form, 'date_input') else ''
            title = 'FACTURE PROFORMA'

        products = []
        for pid in selected_products:
            p = db_manager.get_product_by_id(pid)
            if p:
                products.append(p)

        total = sum(float(p.get('subtotal', 0) or 0) for p in products)
        total_formatted = f"{total:,.2f}".replace(",", " ")

        header = f"<h2>{title}</h2>"
        if invoice_type == 'standard':
            header += f"<p><strong>Date émission:</strong> {date_issue} &nbsp;&nbsp; <strong>Date résultat:</strong> {date_result}</p>"
            header += f"<p><strong>Ref produit:</strong> {form.product_ref_input.text() if hasattr(form, 'product_ref_input') else ''}</p>"
        else:
            header += f"<p><strong>Date:</strong> {date}</p>"

        header += f"<p><strong>Client:</strong> {company_name}<br><strong>Responsable:</strong> {responsable}<br><strong>STAT:</strong> {stat}<br><strong>NIF:</strong> {nif}<br><strong>Adresse:</strong> {address}</p>"

        # Table header selon type
        if invoice_type == 'standard':
            columns = ['Désignation', 'Ref.b.analyse', 'N°Acte', 'Physico', 'Toxico', 'Micro', 'Sous-total']
        else:
            columns = ['Désignation', 'N°Acte', 'Physico', 'Toxico', 'Micro', 'Sous-total']

        table = '<table class="invoice-table" border="1" cellspacing="0" cellpadding="4" width="100%">'
        table += '<tr class="invoice-table-header">'
        for col in columns:
            table += f'<th>{col}</th>'
        table += '</tr>'

        for prod in products:
            table += '<tr>'
            table += f"<td>{prod.get('product_name','')}</td>"
            if invoice_type == 'standard':
                table += f"<td>{prod.get('ref_b_analyse','')}</td>"
            table += f"<td>{prod.get('num_act','')}</td>"
            table += f"<td>{prod.get('physico','')}</td>"
            table += f"<td>{prod.get('toxico','')}</td>"
            table += f"<td>{prod.get('micro','')}</td>"
            table += f"<td>{prod.get('subtotal','')}</td>"
            table += '</tr>'

        table += '</table>'

        footer = '<div class="invoice-footer">'
        footer += f"<p>Total: {total_formatted} Ariary</p>"
        footer += '<p>Arrêté la présente facture à la somme de : Ariary</p>'
        footer += '<p>Mode de paiement: Espèces / Chèque</p>'
        footer += '<p>Le Client ______________________ Le(a) Caissier(e) ______________________</p>'
        footer += '</div>'

        css = self._load_print_css()

        html = '<html><head><meta charset="UTF-8">'
        html += f"<style>{css}</style>"
        html += '</head><body>'
        html += '<div class="invoice-root">'
        html += '<h1 class="invoice-title">AGENCE DE CONTRÔLE DE LA SÉCURITÉ SANITAIRE ET DE LA QUALITÉ DES DENRÉES ALIMENTAIRES</h1>'
        html += header + table + footer
        html += '</div></body></html>'

        return html

    def preview_invoice(self, html):
        if not html:
            QMessageBox.warning(self.parent, 'Aperçu impossible', 'Impossible de générer l’aperçu. Vérifiez les données.')
            return

        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageLayout(
            QPageLayout(
                QPageSize(QPageSize.A4),
                QPageLayout.Portrait,
                QMarginsF(12, 12, 12, 12)
            )
        )

        def render_preview(p):
            doc = QTextDocument()
            doc.setHtml(html)
            doc.print_(p)

        preview = QPrintPreviewDialog(printer, self.parent)
        preview.setWindowTitle('Aperçu de la facture')
        preview.paintRequested.connect(render_preview)
        preview.exec()

    def print_invoice(self, html):
        if not html:
            QMessageBox.warning(self.parent, 'Impression impossible', 'Impossible de générer l’impression. Vérifiez les données.')
            return

        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageLayout(
            QPageLayout(
                QPageSize(QPageSize.A4),
                QPageLayout.Portrait,
                QMarginsF(12, 12, 12, 12)
            )
        )

        dialog = QtWidgets.QPrintDialog(printer, self.parent)
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            doc = QTextDocument()
            doc.setHtml(html)
            doc.print_(printer)
from pathlib import Path
from html import escape

from PySide6 import QtWidgets
from PySide6.QtCore import QMarginsF
from PySide6.QtGui import QTextDocument, QPageSize, QPageLayout
from PySide6.QtWidgets import QMessageBox
from PySide6.QtPrintSupport import QPrinter, QPrintPreviewDialog

from utils.text_utils import TextUtils


class InvoicePrinter:
    def __init__(self, parent_widget):
        self.parent = parent_widget

    def _resolve_logo_src(self):
        logo_path = Path(__file__).resolve().parent.parent / "images" / "logo_acssqda.png"
        return logo_path.as_uri() if logo_path.exists() else ""

    def _load_print_css(self):
        try:
            with open("styles/invoice_print.css", "r", encoding="utf-8") as css_file:
                return css_file.read()
        except FileNotFoundError:
            return ""

    def generate_invoice_html(self, form, invoice_type, selected_products, db_manager):
        company_name    = form.company_name_input.text().strip()
        responsable     = form.responsable_input.text().strip()
        stat            = form.stat_input.text().strip()
        nif             = form.nif_input.text().strip()
        address         = form.address_input.text().strip() if hasattr(form, 'address_input') else ""

        if invoice_type == 'standard':
            date_issue      = form.date_issue_input.date().toString('dd/MM/yyyy') if hasattr(form, 'date_issue_input') else ''
            date_result     = form.date_result_input.date().toString('dd/MM/yyyy') if hasattr(form, 'date_result_input') else ''
            product_ref_raw = form.product_ref_input.text() if hasattr(form, 'product_ref_input') else ''
            title           = 'FACTURE'
        else:
            date_issue      = form.date_input.date().toString('dd/MM/yyyy') if hasattr(form, 'date_input') else ''
            date_result     = ''
            product_ref_raw = ''
            title           = 'FACTURE PROFORMA'

        products        = [db_manager.get_product_by_id(pid) for pid in selected_products if db_manager.get_product_by_id(pid)]
        total           = sum(float(p.get('subtotal', 0) or 0) for p in products)
        total_formatted = f"{total:,.0f}".replace(',', '\u00a0')
        total_words     = TextUtils.number_to_words(round(total)).lower()

        company_name = escape(company_name)
        responsable  = escape(responsable)
        stat         = escape(stat)
        nif          = escape(nif)
        address      = escape(address)
        issue_label  = escape(date_issue)
        result_label = escape(date_result)
        product_ref  = escape(product_ref_raw)

        logo_src = self._resolve_logo_src()
        logo_tag = (f'<img src="{logo_src}" width="75" height="65">'
                    if logo_src else '<span style="display:inline-block;width:75px;height:65px;"></span>')

        # ---- ENTÊTE: tableau HTML 2 colonnes (agency | DOIT box) ----
        header = f"""
<table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tr>
    <td width="56%" valign="top" style="padding-right:8pt;">
      <table cellspacing="0" cellpadding="0" border="0" width="100%">
        <tr>
          <td width="80" valign="top">{logo_tag}</td>
          <td valign="top" style="border-top:1px solid #000;border-bottom:1px solid #000;
              padding:3pt 3pt 3pt 8pt;font-size:11pt;font-weight:bold;
              text-transform:uppercase;line-height:1.3;">
            AGENCE DE CONTR&#xD4;LE DE<br>
            LA SECURITE SANITAIRE<br>
            ET DE LA QUALITE DES<br>
            DENREES ALIMENTAIRES
          </td>
        </tr>
      </table>
      <table cellspacing="0" cellpadding="1" border="0" style="margin-top:4pt;">
        <tr>
          <td style="width:50pt;font-style:italic;font-size:9pt;">NIF:</td>
          <td style="font-style:italic;font-size:9pt;">2001451249</td>
        </tr>
        <tr>
          <td style="font-style:italic;font-size:9pt;">STAT:</td>
          <td style="font-style:italic;font-size:9pt;">86,909,112,006,001,800</td>
        </tr>
        <tr>
          <td style="font-style:italic;font-size:9pt;">TEL:</td>
          <td style="font-style:italic;font-size:9pt;">22 222 39</td>
        </tr>
        <tr>
          <td style="font-style:italic;font-size:9pt;">Adresse:</td>
          <td style="font-style:italic;font-size:9pt;">Rue Karidja Tsaralalàna<br>
          (Ex Bâtiment Pharmacie Centrale Face Hôtel de Police)</td>
        </tr>
      </table>
    </td>
    <td width="44%" valign="top" style="border:1px solid #000;padding:0;">
      <table width="100%" cellspacing="0" cellpadding="0" border="0">
        <tr>
          <td align="center" style="font-size:13pt;font-weight:bold;padding:3pt 0;
              border-bottom:1px solid #000;">DOIT</td>
        </tr>
        <tr>
          <td style="padding:4pt 8pt;">
            <p style="font-style:italic;font-size:9pt;margin:0 0 9pt 0;">Raison social:&nbsp; {company_name}</p>
            <p style="font-style:italic;font-size:9pt;margin:0 0 9pt 0;">Statistique: {stat}</p>
            <p style="font-style:italic;font-size:9pt;margin:0 0 9pt 0;">NIF: {nif}</p>
            <p style="font-style:italic;font-size:9pt;margin:0;">Adresse: {address}</p>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
<h2 style="text-align:center;font-style:italic;font-weight:bold;font-size:17pt;margin:5pt 0;">{title}</h2>
"""

        # ---- TABLEAU PRINCIPAL: 7 colonnes, en-tête meta avec colspan (1+1+2+2+1=7) ----
        hs = 'font-weight:normal;font-style:italic;font-size:9pt;'
        rows = ''
        for prod in products:
            ref_b    = escape(str(prod.get('ref_b_analyse', '') or ''))
            desig    = escape(str(prod.get('product_name',  '') or ''))
            num_act  = escape(str(prod.get('num_act',       '') or ''))
            physico  = escape(str(prod.get('physico',       '') or ''))
            micro    = escape(str(prod.get('micro',         '') or ''))
            toxico   = escape(str(prod.get('toxico',        '') or ''))
            subtotal = escape(str(prod.get('subtotal',      '') or ''))
            rows += (f'<tr>'
                     f'<td>{ref_b}</td>'
                     f'<td>{desig}</td>'
                     f'<td>{num_act}</td>'
                     f"<td style='text-align:right;'>{physico}</td>"
                     f"<td style='text-align:right;'>{micro}</td>"
                     f"<td style='text-align:right;'>{toxico}</td>"
                     f"<td style='text-align:right;'>{subtotal}</td>"
                     f'</tr>')

        table = f"""
<table class="invoice-table" cellspacing="0" cellpadding="3">
  <thead>
    <tr>
      <th style="width:10%;{hs}">Numéro</th>
      <th style="width:26%;{hs}">Date d'émission</th>
      <th style="width:24%;{hs}" colspan="2">Référence(s) des produits</th>
      <th style="width:24%;{hs}" colspan="2">Date du résultat</th>
      <th style="width:16%;{hs}">Responsable</th>
    </tr>
    <tr>
      <th style="width:10%;{hs}">Réf.<br>Bulletin<br>d'analyse</th>
      <th style="width:26%;{hs}">Désignations</th>
      <th style="width:12%;{hs}">N°Acte de<br>prélèvement</th>
      <th style="width:12%;{hs}">Physico<br>chimique</th>
      <th style="width:12%;{hs}">Micro-<br>biologique</th>
      <th style="width:12%;{hs}">Toxico-<br>logique</th>
      <th style="width:16%;{hs}">Sous-total</th>
    </tr>
    <tr style="font-style:italic;font-size:9pt;">
      <td>&nbsp;</td>
      <td>{issue_label}</td>
      <td colspan="2">{product_ref}</td>
      <td colspan="2">{result_label}</td>
      <td>{responsable}</td>
    </tr>
  </thead>
  <tbody>
{rows}
  </tbody>
  <tfoot>
    <tr style="font-style:italic;font-size:9pt;">
      <td colspan="5" style="text-align:right;">Montant à payer</td>
      <td style="text-align:right;">{total_formatted}</td>
      <td style="text-align:right;">Ar</td>
    </tr>
  </tfoot>
</table>
"""

        # ---- PIED DE PAGE ----
        footer = f"""
<div class="invoice-footer">
  <p style="margin:6pt 0 4pt;">Arrêtée la présente facture à la somme de&nbsp;: {escape(total_words)} Ariary</p>
  <p style="margin:4pt 0;">Mode de paiement
    <span style="margin-left:24pt;">Espèces</span>
    <span style="margin-left:36pt;">Chèque</span>
  </p>
  <table width="100%" cellspacing="0" cellpadding="0" border="0" style="margin-top:20pt;">
    <tr>
      <td align="center" style="font-size:9pt;">Le Client</td>
      <td align="center" style="font-size:9pt;">Le(a) Caissier(e)</td>
    </tr>
  </table>
  <table width="100%" cellspacing="0" cellpadding="0" border="0" style="margin-top:18pt;">
    <tr>
      <td style="font-size:9pt;">(*) Chèque visé à l'ordre de Madame le RECEVEUR GENERAL .</td>
      <td align="right" style="font-size:9pt;">Quittance N°</td>
    </tr>
  </table>
</div>
"""

        css = self._load_print_css()
        return f"""<!DOCTYPE HTML>
<html>
<head>
  <meta charset="UTF-8">
  <style>{css}</style>
</head>
<body>
<div class="invoice-root">
{header}
{table}
{footer}
</div>
</body>
</html>"""


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
"""
Génération HTML et impression des certificats CC / CNC.

Chaque certificat occupe une page A4 portrait.
L'impression utilise QPrinter / QPrintDialog (même approche que InvoicePrinter).
"""
from pathlib import Path
from html import escape

from PySide6.QtGui import QTextDocument, QPageSize, QPageLayout
from PySide6.QtCore import QMarginsF
from PySide6.QtPrintSupport import QPrinter, QPrintDialog


# Textes du corps selon le type de certificat
_BODY_TEXT = {
    "CC": (
        "Nous, soussignés, certifions que le produit désigné ci-dessus a été soumis aux analyses "
        "physico-chimiques, microbiologiques et toxicologiques conformément aux normes en vigueur. "
        "Les résultats de ces analyses révèlent que ledit produit est "
        "<b>CONSOMMABLE</b> et répond aux exigences de qualité et de salubrité requises."
    ),
    "CNC": (
        "Nous, soussignés, certifions que le produit désigné ci-dessus a été soumis aux analyses "
        "physico-chimiques, microbiologiques et toxicologiques conformément aux normes en vigueur. "
        "Les résultats de ces analyses révèlent que ledit produit est "
        "<b>NON CONSOMMABLE</b> et ne répond pas aux exigences de qualité et de salubrité requises."
    ),
}

_TITLES = {
    "CC":  "CERTIFICAT DE CONSOMMABILITÉ",
    "CNC": "CERTIFICAT DE NON CONSOMMABILITÉ",
}


class CertificatePrinter:
    """
    Convertit une liste d'assignations (pid, product_name, cert_type)
    en HTML imprimable et lance le dialogue d'impression.
    """

    def __init__(self, parent_widget):
        self.parent = parent_widget

    # ------------------------------------------------------------------
    # Ressources
    # ------------------------------------------------------------------

    def _resolve_logo_src(self) -> str:
        logo_path = Path(__file__).resolve().parent.parent.parent / "images" / "image.png"
        return logo_path.as_uri() if logo_path.exists() else ""

    def _load_css(self) -> str:
        try:
            with open("styles/certificate_print.css", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    # ------------------------------------------------------------------
    # Extraction des données du formulaire
    # ------------------------------------------------------------------

    def _extract_form_data(self, form) -> dict:
        """Lit les champs du formulaire client actif et échappe les valeurs HTML."""
        if hasattr(form, "date_issue_input"):
            date_str = form.date_issue_input.date().toString("dd/MM/yyyy")
        elif hasattr(form, "date_input"):
            date_str = form.date_input.date().toString("dd/MM/yyyy")
        else:
            date_str = ""

        return {
            "company_name": escape(form.company_name_input.text().strip()),
            "responsable":  escape(form.responsable_input.text().strip()),
            "stat":         escape(form.stat_input.text().strip()),
            "nif":          escape(form.nif_input.text().strip()),
            "address":      escape(
                form.address_input.text().strip() if hasattr(form, "address_input") else ""
            ),
            "date":         escape(date_str),
        }

    # ------------------------------------------------------------------
    # Génération HTML
    # ------------------------------------------------------------------

    def _render_single_certificate(
        self,
        cert_type: str,
        product_name: str,
        fd: dict,
        logo_tag: str,
        is_last: bool,
    ) -> str:
        """
        Génère le fragment HTML d'un seul certificat.

        Paramètres
        ----------
        cert_type    : 'CC' ou 'CNC'
        product_name : désignation du produit
        fd           : dict des données client (clés: company_name, nif, …)
        logo_tag     : balise <img> du logo ou chaîne vide
        is_last      : True pour le dernier certificat (pas de saut de page final)
        """
        title      = escape(_TITLES[cert_type])
        body_text  = _BODY_TEXT[cert_type]
        desig      = escape(product_name)
        page_break = "auto" if is_last else "always"

        return f"""
<div style="page-break-after:{page_break};padding:22pt 30pt;
            font-family:'Times New Roman',serif;font-size:11pt;color:#000;">

  <!-- En-tête: logo + nom de l'agence -->
  <table width="100%" cellspacing="0" cellpadding="0" border="0"
         style="border-bottom:2.5px solid #000;padding-bottom:8pt;margin-bottom:18pt;">
    <tr>
      <td width="14%" valign="middle" style="text-align:center;padding-right:10pt;">
        {logo_tag}
      </td>
      <td width="86%" valign="middle"
          style="padding-left:14pt;font-size:12pt;font-weight:bold;
                 text-transform:uppercase;line-height:1.55;
                 border-left:1.5px solid #ccc;">
        AGENCE DE CONTRÔLE DE LA SÉCURITÉ SANITAIRE<br>
        ET DE LA QUALITÉ DES DENRÉES ALIMENTAIRES
      </td>
    </tr>
  </table>

  <!-- Titre du certificat -->
  <p style="text-align:center;font-size:16pt;font-weight:bold;font-style:italic;
            text-decoration:underline;border:2px solid #000;
            padding:8pt;margin-bottom:22pt;">
    {title}
  </p>

  <!-- Informations client -->
  <table width="100%" cellspacing="0" cellpadding="5" border="0"
         style="margin-bottom:20pt;">
    <tr>
      <td width="34%" style="font-weight:bold;font-style:italic;">Raison sociale :</td>
      <td style="border-bottom:1px solid #bbb;">{fd['company_name']}</td>
    </tr>
    <tr>
      <td style="font-weight:bold;font-style:italic;">NIF :</td>
      <td style="border-bottom:1px solid #bbb;">{fd['nif']}</td>
    </tr>
    <tr>
      <td style="font-weight:bold;font-style:italic;">STAT :</td>
      <td style="border-bottom:1px solid #bbb;">{fd['stat']}</td>
    </tr>
    <tr>
      <td style="font-weight:bold;font-style:italic;">Adresse :</td>
      <td style="border-bottom:1px solid #bbb;">{fd['address']}</td>
    </tr>
    <tr>
      <td style="font-weight:bold;font-style:italic;">Responsable :</td>
      <td style="border-bottom:1px solid #bbb;">{fd['responsable']}</td>
    </tr>
    <tr>
      <td style="font-weight:bold;font-style:italic;">Date :</td>
      <td style="border-bottom:1px solid #bbb;">{fd['date']}</td>
    </tr>
  </table>

  <!-- Encadré Désignation du produit -->
  <table width="100%" cellspacing="0" cellpadding="0"
         style="border:2px solid #000;margin-bottom:22pt;">
    <tr>
      <td style="padding:5pt 12pt;font-style:italic;font-weight:bold;font-size:10pt;
                 border-bottom:1px solid #888;">
        Désignation du produit :
      </td>
    </tr>
    <tr>
      <td style="padding:10pt 12pt;font-size:13pt;font-weight:bold;text-align:center;">
        {desig}
      </td>
    </tr>
  </table>

  <!-- Corps du certificat -->
  <p style="text-align:justify;line-height:1.9;margin-bottom:46pt;font-size:11pt;">
    {body_text}
  </p>

  <!-- Signatures -->
  <table width="100%" cellspacing="0" cellpadding="0" border="0">
    <tr>
      <td width="38%" style="text-align:center;">
        <p style="font-style:italic;margin-bottom:42pt;">Le Responsable</p>
        <hr style="border:none;border-top:1px solid #000;"/>
      </td>
      <td width="24%"></td>
      <td width="38%" style="text-align:center;">
        <p style="font-style:italic;margin-bottom:42pt;">Le Directeur</p>
        <hr style="border:none;border-top:1px solid #000;"/>
      </td>
    </tr>
  </table>

</div>
"""

    def generate_html(self, form, assignments: list[tuple]) -> str:
        """
        Assemble le document HTML complet (tous les certificats, un par page).

        Paramètres
        ----------
        form        : formulaire client actif
        assignments : liste de (pid, product_name, cert_type)
        """
        logo_src = self._resolve_logo_src()
        logo_tag = (
            f'<img src="{logo_src}" width="80" height="70">'
            if logo_src
            else '<span style="display:inline-block;width:80px;height:70px;"></span>'
        )

        fd  = self._extract_form_data(form)
        css = self._load_css()

        pages = [
            self._render_single_certificate(
                cert_type, product_name, fd, logo_tag, i == len(assignments) - 1
            )
            for i, (pid, product_name, cert_type) in enumerate(assignments)
        ]

        return (
            f"<!DOCTYPE HTML><html>"
            f"<head><meta charset='UTF-8'><style>{css}</style></head>"
            f"<body>{''.join(pages)}</body></html>"
        )

    # ------------------------------------------------------------------
    # Impression
    # ------------------------------------------------------------------

    def print_certificates(self, form, assignments: list[tuple]):
        """Affiche le dialogue d'impression et imprime tous les certificats."""
        html = self.generate_html(form, assignments)

        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPageSize(QPageSize.A4))
        printer.setPageOrientation(QPageLayout.Portrait)
        printer.setPageMargins(QMarginsF(10, 10, 10, 10), QPageLayout.Millimeter)

        dlg = QPrintDialog(printer, self.parent)
        if dlg.exec() != QPrintDialog.Accepted:
            return

        doc = QTextDocument()
        doc.setHtml(html)
        doc.print_(printer)

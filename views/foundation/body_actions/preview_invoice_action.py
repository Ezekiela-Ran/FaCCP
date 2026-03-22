from PySide6.QtWidgets import QMessageBox

from views.foundation.globals import GlobalVariable


class PreviewInvoiceAction:
    @staticmethod
    def execute(body_layout):
        main_layout = body_layout.parent()
        if not hasattr(main_layout, "head_layout") or not hasattr(main_layout.head_layout, "form"):
            QMessageBox.warning(
                body_layout,
                "Aperçu impossible",
                "Impossible de générer l’aperçu. Vérifiez les données.",
            )
            return

        form = main_layout.head_layout.form
        selected_products = [
            pid for pid, selected in body_layout.product_manager.selected_products.items() if selected
        ]
        if not selected_products:
            QMessageBox.warning(body_layout, "Aperçu impossible", "Aucun produit sélectionné.")
            return

        html = body_layout.invoice_printer.generate_invoice_html(
            form,
            GlobalVariable.invoice_type,
            selected_products,
            body_layout.db_manager,
        )
        body_layout.invoice_printer.preview_invoice(html)

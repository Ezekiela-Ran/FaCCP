class CalculateTotalAction:
    @staticmethod
    def execute(body_layout):
        total = 0.0
        for pid, selected in body_layout.product_manager.selected_products.items():
            if not selected:
                continue
            product = body_layout.product_service.get_product_by_id(pid)
            if product and "subtotal" in product:
                try:
                    total += float(product["subtotal"] or 0)
                except (TypeError, ValueError):
                    pass
        return total

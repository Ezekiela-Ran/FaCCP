class UpdateTotalDisplayAction:
    @staticmethod
    def execute(body_layout):
        total = body_layout.calculate_total()
        total_words = body_layout.number_to_words(int(total)) + " ARIARY"
        formatted_total = f"{total:,.2f}".replace(",", " ")
        body_layout.net_a_payer_label.setText(
            f"Net à payer: {formatted_total} Ariary ({total_words})"
        )

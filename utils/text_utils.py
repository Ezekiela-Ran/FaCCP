from num2words import num2words


class TextUtils:
    @staticmethod
    def number_to_words(number):
        try:
            value = int(number)
        except (TypeError, ValueError):
            value = 0

        words = num2words(value, lang="fr")
        return words.upper().replace("-", " ")
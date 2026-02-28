from PySide6 import QtWidgets
class ListLayout(QtWidgets.QWidget):
    """
    Widget principal qui contient MenuLayout et éventuellement d'autres widgets.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

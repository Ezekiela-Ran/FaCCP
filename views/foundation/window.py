from PySide6 import QtWidgets

class Window(QtWidgets.QWidget):
    
    """
        Voici la fenêtre principale et ses configurations
    """
    def __init__(self):
        super().__init__()
        
        height = self.screen().size().height()
        width = self.screen().size().width()
        
        self.setWindowTitle("Acssqda")
        self.setGeometry(0, 0, width, height)
        self.window_layout = QtWidgets.QVBoxLayout(self)
        self.window_layout.setContentsMargins(0, 0, 0, 0)
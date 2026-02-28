"""
    This is the main entry point of the application
"""
import sys
from PySide6 import QtWidgets
from views.foundations.windows import Window
from views.components.menu import MenuComponent
      

if __name__ == "__main__":
    
    app = QtWidgets.QApplication([])

    win = Window()

    menu = MenuComponent(win)
    
    win.show()

    sys.exit(app.exec())


from PySide6.QtWidgets import (QWidget, QVBoxLayout)
from views.foundation.head_layout import HeadLayout
from views.foundation.body_layout import BodyLayout
from views.components.menu_bar import MenuBar

class MainLayout(QWidget):
    def __init__(self,parent):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        menu_bar = MenuBar(self)
        self.layout.addWidget(menu_bar)

        self.head_layout = HeadLayout(self)
        self.head_layout.standard_invoice()
        self.body_layout = BodyLayout(self)

        self.layout.addWidget(self.head_layout, stretch=1)
        self.layout.addWidget(self.body_layout, stretch=1)

    def menubar_click_standard(self):
        self.clear_layout()

        menu_bar = MenuBar(self)
        self.layout.addWidget(menu_bar)

        self.head_layout = HeadLayout(self)
        self.head_layout.standard_invoice()
        self.body_layout = BodyLayout(self)

        self.layout.addWidget(self.head_layout, stretch=1)
        self.layout.addWidget(self.body_layout, stretch=1)

    def menubar_click_proforma(self):
        self.clear_layout()

        menu_bar = MenuBar(self)
        self.layout.addWidget(menu_bar)

        self.head_layout = HeadLayout(self)
        self.head_layout.proforma_invoice()
        self.body_layout = BodyLayout(self)

        self.layout.addWidget(self.head_layout, stretch=1)
        self.layout.addWidget(self.body_layout, stretch=1)


    def clear_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_sub_layout(child.layout())



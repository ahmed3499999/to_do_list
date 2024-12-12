from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt5 import *
from PyQt5.QtWidgets import *
import sys
from . import colors as c

class PinButton(QPushButton):
    style = """
    QPushButton{
        border: none;
        padding:5;
        margin:0;
        background-color: %s;
    }
    QPushButton:hover{
        background-color: %s;
    }
    """ % (c.sidebar_bg, c.sidebar_items_hover)
    pinToggled = pyqtSignal(bool)
    def __init__(self, text = None, parent = None):
        super().__init__(text, parent)
        self.isActive = False
        self.enabledIcon = QIcon('icons/blue_pin.svg')
        self.disableIcon = QIcon('icons/pin.svg')
        self.pressed.connect(self.toggleIcon)

        self.setStyleSheet(self.style)
        self.setIcon(self.disableIcon)
        self.setIconSize(QSize(17, 17))

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.pinToggled.emit(self.isActive)

    def toggleIcon(self):
        if self.isActive:
            self.isActive = False
            self.setIcon(self.disableIcon)
        else:
            self.isActive = True
            self.setIcon(self.enabledIcon)

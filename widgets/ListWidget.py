from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt5 import *
from PyQt5.QtWidgets import *
from .PinButton import PinButton
from .colors import *
from task_list import *

class ListLineEdit(QLineEdit):
    style = """
    background-color: '%s';
    border-style: none;
    border-radius: 1;
    font-family: 'ui-sans-serif';
    font-size:18px;
    margin: 5px;
    padding-left: 5px;
    padding-top: 10px;
    padding-bottom: 10px;
    padding-right: 10px;
    color: %s
    """
    clicked = pyqtSignal()

    def __init__(self, text = None, parent = None):
        super(ListLineEdit, self).__init__(text, parent)
        
        self.isEditing = False
        self.isSelected = False
        self.setStyleSheet(self.style % (sidebar_bg, secondary_text))
        self.setMouseTracking(True)
        self.setReadOnly(True)
        #disable selection
        self.selectionChanged.connect(self.ResetSelection)
        self.editingFinished.connect(self.finishEditing)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.clicked.emit()
    
    def enterEvent(self, event):
        super().enterEvent(event)
        if self.isSelected:
            self.setStyleSheet(self.style % (primary_button, primary_text))
        else:
            self.setStyleSheet(self.style % (sidebar_items_hover, secondary_text))

    def leaveEvent(self, event):
        super().leaveEvent(event)
        if self.isSelected:
            self.setStyleSheet(self.style % (primary_button, primary_text))
        else:
            self.setStyleSheet(self.style % (sidebar_bg, secondary_text))

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        self.isEditing = True
        self.setReadOnly(False)
        self.setFocus()
        self.setSelection(0, len(self.text()))

    def finishEditing(self):
        self.setReadOnly(True)
        self.isEditing = False

    def ResetSelection(self):
        if self.isEditing: return
        self.setSelection(0, 0)

    def ToggleActive(self):
        self.isSelected = True
        self.setStyleSheet(self.style % (primary_button, primary_text))

    def ToggleInactive(self):
        self.isSelected = False
        self.setStyleSheet(self.style % (sidebar_bg, secondary_text))
        self.finishEditing()

class ListWidget(QWidget):
    selected = pyqtSignal(QObject)
    pinToggled = pyqtSignal(bool)
    nameChanged = pyqtSignal(str)
    instances = []
    
    def __init__(self, listData: TaskList):
        super(ListWidget, self).__init__()
        self.listData = listData
        self.setStyleSheet('padding:0; margin: 0')
        self.line = ListLineEdit(listData.name)
        self.line.clicked.connect(self.ToggleActive)
        self.line.clicked.connect(lambda: self.selected.emit(self))
        self.line.editingFinished.connect(lambda: self.nameChanged.emit(self.line.text()))
        self.line.editingFinished.connect(lambda: setattr(self.listData, 'name', self.line.text()))

        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.btn = PinButton()
        if listData.pinned:
            self.btn.toggleIcon()
        self.pinToggled = self.btn.pinToggled

        layout.addWidget(self.line)
        layout.addWidget(self.btn)

        self.instances.append(self)
        self.ToggleActive()
    
    def ToggleActive(self):
        for i in self.instances:
            i.ToggleInactive()
        self.isSelected = True
        self.line.ToggleActive()
        self.selected.emit(self)

    def ToggleInactive(self):
        self.isSelected = False
        self.line.ToggleInactive()
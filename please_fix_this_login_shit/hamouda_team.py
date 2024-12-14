from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt5 import *
from PyQt5.QtWidgets import *

import sys


listBtnStyle = """
background-color: '%s';
border-style: none;
border-radius: 1;
font-family: 'ui-sans-serif';
font-size:20px;
margin: 5px;
padding-left: 5px;
padding-top: 10px;
padding-bottom: 10px;
padding-right: 10px;
color: %s
"""
listBtnDefault = '#F3F4F6'
listBtnActive = '#3B82F6'
listBtnHover = '#E5E7EB'
textPrimary = '#111827'
textSecondary= '#374151'
textActive = 'white'


class SignaledLineEdit(QLineEdit):
    pressed = pyqtSignal()
    doubleClicked = pyqtSignal()
    mouseEntered = pyqtSignal()
    mouseLeft  = pyqtSignal()
    
    def __init__(self, text = None, parent = None):
        super().__init__(text, parent)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.pressed.emit()    
    
    def enterEvent(self, event):
        super().enterEvent(event)
        self.mouseEntered.emit()    

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.mouseLeft.emit()

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        self.doubleClicked.emit()

class ListWidget(QWidget):
    selected = pyqtSignal(QObject)
    instances = []
    
    def __init__(self, text):
        super(ListWidget, self).__init__()
        self.setStyleSheet('padding:0; margin: 0')

        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.isEditing = False
        self.isSelected = False
        self.line = SignaledLineEdit(text)
        self.line.setStyleSheet(listBtnStyle % (listBtnDefault, textPrimary))
        self.line.setMouseTracking(True)
        self.line.setReadOnly(True)
        #disable selection
        self.line.selectionChanged.connect(self.ResetSelection)
        self.line.doubleClicked.connect(self.onDoubleClicked)
        self.line.editingFinished.connect(self.onTextEdited)
        self.line.mouseEntered.connect(self.onMouseEnter)
        self.line.mouseLeft.connect(self.onMouseLeave)
        self.line.pressed.connect(self.onPressed)

        self.btn = QPushButton()
        self.btn.setStyleSheet('padding:0; margin:0')
        self.btn.setStyleSheet("QPushButton { background-color: #F0F0F0;border: none; }")
        self.btn.setIcon(QIcon('pin.png'))

        layout.addWidget(self.line)
        layout.addWidget(self.btn)

        self.instances.append(self)
    
    def ResetSelection(self):
        if self.isEditing: return
        self.line.setSelection(0, 0)
    
    def ToggleActive(self):
        for i in self.instances:
            i.ToggleInactive()
        self.isSelected = True

    def ToggleInactive(self):
        self.isSelected = False
        self.line.setStyleSheet(listBtnStyle % (listBtnDefault, textPrimary))


    def onDoubleClicked(self):
        self.line.setReadOnly(False)
        self.line.setFocus()
        self.isEditing = True
    
    def onTextEdited(self):
        self.line.setReadOnly(True)
        self.isEditing = False
        print("shit edited")

    def onPressed(self):
        self.selected.emit(self)
        for i in self.instances:
            i.ToggleInactive()
        self.ToggleActive()
        self.line.setStyleSheet(listBtnStyle % (listBtnActive, textActive))

    def onMouseEnter(self):
        if self.isSelected:
            self.line.setStyleSheet(listBtnStyle % (listBtnActive, textActive))
        else:
            self.line.setStyleSheet(listBtnStyle % (listBtnHover, textSecondary))

    def onMouseLeave(self):
        if self.isSelected:
            self.line.setStyleSheet(listBtnStyle % (listBtnActive, textActive))
        else:
            self.line.setStyleSheet(listBtnStyle % (listBtnDefault, textPrimary))

class Window(QMainWindow):
    def handle_add_Button(self):
        self.scrollLayout.addWidget(ListWidget('New List'))
    
    def handle_delete_Button(self):
        self.scrollLayout.removeWidget(self.selected)
        self.selected.setParent(None)
        
    def handle_selected(self, widget):
        self.selected = widget
        # print(widget.line.text())
    
    def __init__(self):
        super(Window, self).__init__()
        self.setStyleSheet("background-color: '#F3F4F6'")
        list = [ListWidget('My List ' + str(x)) for x in range(1,4)]
        self.selected =''

        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)
        self.setCentralWidget(container)
        scroll = QScrollArea(self)
        layout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        ##########################
        button = QPushButton('ADD')
        layout.addWidget(button)
        button.clicked.connect(self.handle_add_Button)
        ##########################
        button = QPushButton('Delete')
        layout.addWidget(button)
        button.clicked.connect(self.handle_delete_Button)
        ##########################
        self.scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(self.scrollLayout)
        for item in list:
            self.scrollLayout.addWidget(item)
            item.selected.connect(self.handle_selected)
        self.scrollLayout.addStretch()
        scroll.setWidget(scrollContent)

def main():
   app = QApplication(sys.argv)
   ex = Window()
   ex.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
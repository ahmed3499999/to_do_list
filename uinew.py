from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt5 import *
from PyQt5.QtWidgets import *
import sys

class Window(QMainWindow):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self.box = QComboBox()
        self.box.addItem('fuck you seif')
        self.box.addItem('fuck you seif again')
        

        layout = QVBoxLayout()
        layout.addWidget(self.box)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

def main():
   app = QApplication(sys.argv)
   ex = Window()
   ex.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
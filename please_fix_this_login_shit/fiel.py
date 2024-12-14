from PyQt5 import QtWidgets, QtCore

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.button = QtWidgets.QPushButton('Test')
        self.button.clicked.connect(self.handleButton)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button)

    def handleButton(self):
        print('Hello World')

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
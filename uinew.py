from PyQt5 import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt5 import *
from PyQt5.QtWidgets import *
import sys
from widgets.PinButton import PinButton
from widgets.colors import *
from widgets.ListWidget import ListWidget
from widgets.TaskWidget import TaskWidget


class Window(QMainWindow):
    scrollAreaStyle = """
     QScrollArea {
        border: none;
    }
    QScrollBar:vertical {
        background: transparent;
        width: 14px;
        margin: 4px;
    }

    QScrollBar::handle:vertical {
        background: #5A5A5A;
        border-radius: 15px;
        min-height: 20px;
        min-width: 20px;
    }
    QScrollBar::handle:vertical:hover {
        background: #3A3A3A;
    }
    QScrollBar::add-line, QScrollBar::sub-line {
        background: none;
        border: none;
    }
    """

    listBtnStyle = """
    QPushButton{
        border: none;
        background-color: '%s';
        font-family: 'ui-sans-serif';
        font-size: 16px;
        padding: 10px;
        border-radius: 5px;
        color: %s;
    }
    QPushButton:hover{
    background-color: '%s';
    }
    """ 

    taskBtnStyle = """
    QPushButton{
        border: none;
        background-color: '%s';
        font-family: 'ui-sans-serif';
        font-size: 15px;
        padding: 11px;
        margin-bottom: 9px;
        border-radius: 5px;
        color: %s;
    }
    QPushButton:hover{
    background-color: '%s';
    }
    """ 
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        dummyList = [ListWidget('My List ' + str(x)) for x in range(1,5)]
        self.setStyleSheet("background-color: %s;" % main_bg)
        
        mainLayout = QHBoxLayout()
        mainContainer = QFrame()
        mainContainer.setLayout(mainLayout)
        mainLayout.setContentsMargins(0,0,0,0)
        self.setCentralWidget(mainContainer)

        leftContainer = QFrame()
        leftLayout = QVBoxLayout()
        leftContainer.setLayout(leftLayout)
        leftContainer.setStyleSheet("background-color: %s;" % sidebar_bg)
        rightContainer = QFrame()
        rightLayout = QVBoxLayout()
        rightContainer.setLayout(rightLayout)
        rightContainer.setStyleSheet("background-color: '%s'" % main_bg)

        mainLayout.addWidget(leftContainer)
        mainLayout.setStretchFactor(leftContainer, 12)
        mainLayout.addWidget(rightContainer)
        mainLayout.setStretchFactor(rightContainer, 20)

        listsLabel = QLabel(" Your Lists")
        listsLabel.setStyleSheet("color:%s;font-weight: bold;font-size:22px;font-family:'ui-sans-serif'" % primary_text)
        leftLayout.addWidget(listsLabel)

        #task lists area
        self.listsScrollLayout = QVBoxLayout()
        for i in dummyList:
            self.listsScrollLayout.addWidget(i)

        self.listsScrollLayout.addStretch()
        listsScrollArea = QScrollArea()
        listsScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        listsScrollArea.setStyleSheet(self.scrollAreaStyle)
        listsScrollArea.setLayout(self.listsScrollLayout)
        listsScrollArea.setWidgetResizable(True)
        taskListsContainer = QWidget(listsScrollArea)
        taskListsContainer.setLayout(self.listsScrollLayout)
        listsScrollArea.setWidget(taskListsContainer)
        leftLayout.addWidget(listsScrollArea)

        #buttons area
        buttonsLayout = QVBoxLayout()
        self.addListBtn = QPushButton("+ Add List")
        self.addListBtn.setStyleSheet(self.listBtnStyle % (primary_button, primary_text,primary_button_hover))
        self.addListBtn.clicked.connect(self.addNewList)
        self.deleteListBtn = QPushButton("- Delete List")
        self.deleteListBtn.setStyleSheet(self.listBtnStyle % (delete_list_button, primary_text, delete_list_button_hover))

        buttonsLayout.addWidget(self.addListBtn)
        buttonsLayout.addWidget(self.deleteListBtn)

        buttonsContainer = QWidget()
        buttonsContainer.setLayout(buttonsLayout)
        leftLayout.addWidget(buttonsContainer)
        
        tasksTitle = QLabel("Tasks")
        tasksTitle.setStyleSheet("color: %s;font-weight: bold;font-family: 'ui-sans-serif'; font-size: 25px;margin-bottom:8px;" % primary_text)
        rightLayout.addWidget(tasksTitle)

        tasksScrollLayout = QVBoxLayout()
        tasksScrollArea = QScrollArea()
        tasksScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        tasksScrollArea.setStyleSheet(self.scrollAreaStyle)
        tasksScrollArea.setLayout(tasksScrollLayout)
        tasksScrollArea.setWidgetResizable(True)
        taskListsContainer = QWidget(tasksScrollArea)
        taskListsContainer.setLayout(tasksScrollLayout)
        tasksScrollArea.setWidget(taskListsContainer)
        rightLayout.addWidget(tasksScrollArea)
        
        tasksScrollLayout.addWidget(TaskWidget('Buy the thing','2024-03-12', True))
        tasksScrollLayout.addWidget(TaskWidget('Quiz','2024-04-06', False))
        tasksScrollLayout.addWidget(TaskWidget('fuck seif in the ass','2024-09-23', True))  
        tasksScrollLayout.addWidget(TaskWidget('Buy the thing','2024-03-12', True))
        tasksScrollLayout.addWidget(TaskWidget('Quiz','2024-04-06', False))
        tasksScrollLayout.addWidget(TaskWidget('fuck seif in the ass','2024-09-23', True))  
        tasksScrollLayout.addWidget(TaskWidget('Buy the thing','2024-03-12', True))
        tasksScrollLayout.addWidget(TaskWidget('Quiz','2024-04-06', False))
        tasksScrollLayout.addWidget(TaskWidget('fuck seif in the ass','2024-09-23', True))  
        tasksScrollLayout.addStretch()

        self.addTaskBtn = QPushButton("+ Add Task")
        self.addTaskBtn.setStyleSheet(self.taskBtnStyle % (add_task_button, primary_text, add_task_button_hover))
        rightLayout.addWidget(self.addTaskBtn)

    def addNewList(self):
        self.listsScrollLayout.addWidget(ListWidget("New List"))
        

def main():
   app = QApplication(sys.argv)
   ex = Window()
   ex.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
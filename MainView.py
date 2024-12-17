import sys
from PyQt5 import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt5 import *
from PyQt5.QtWidgets import *
from widgets.PinButton import PinButton
from widgets.colors import *
from widgets.ListWidget import ListWidget
from widgets.TaskWidget import TaskWidget
from TaskViewPanel import TaskViewPanel
from task_list import *
from datetime import datetime

class MainView(QMainWindow):
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
    def __init__(self, addTaskCallback, modifyTaskCallback, parent = None):
        super(MainView, self).__init__(parent)
        self.modifyTaskCallback = modifyTaskCallback
        self.addTaskCallback = addTaskCallback
        self.setMinimumWidth(700)
        self.setStyleSheet("background-color: %s;" % main_bg)
        self.selectedList = None

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
        self.addListBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.addListBtn.setStyleSheet(self.listBtnStyle % (primary_button, primary_text,primary_button_hover))
        self.addListBtn.clicked.connect(self.addNewList)
        self.deleteListBtn = QPushButton("- Delete List")
        self.deleteListBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.deleteListBtn.setStyleSheet(self.listBtnStyle % (delete_list_button, primary_text, delete_list_button_hover))
        self.deleteListBtn.clicked.connect(self.removeSelectedList)

        buttonsLayout.addWidget(self.addListBtn)
        buttonsLayout.addWidget(self.deleteListBtn)

        buttonsContainer = QWidget()
        buttonsContainer.setLayout(buttonsLayout)
        leftLayout.addWidget(buttonsContainer)
        
        tasksLabelAndSortLayout = QHBoxLayout()
        tasksLabelAndSortContainer = QWidget()
        tasksLabelAndSortContainer.setLayout(tasksLabelAndSortLayout)
        rightLayout.addWidget(tasksLabelAndSortContainer)

        tasksTitle = QLabel("Tasks")
        tasksTitle.setStyleSheet("color: %s;font-weight: bold;font-family: 'ui-sans-serif'; font-size: 25px;margin-bottom:8px;" % primary_text)
        tasksLabelAndSortLayout.addWidget(tasksTitle)

        self.sortBox = QComboBox()
        self.sortBox.setStyleSheet("""
        color: %s;
        background-color: %s;
        font-weight: bold;
        font-size: 12px;
        padding: 5px;
        padding-left 10px;
        """ % (primary_text, sidebar_bg))
        self.sortBox.addItems(["Sort: Priority","Sort: Alphabet", "Sort: Deadline"])
        self.sortBox.currentTextChanged.connect(lambda t: self.refreshTaskList())
        tasksLabelAndSortLayout.addWidget(self.sortBox)

        self.tasksScrollLayout = QVBoxLayout()
        self.tasksScrollLayout.addStretch()
        tasksScrollArea = QScrollArea()
        tasksScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        tasksScrollArea.setStyleSheet(self.scrollAreaStyle)
        tasksScrollArea.setLayout(self.tasksScrollLayout)
        tasksScrollArea.setWidgetResizable(True)
        taskListsContainer = QWidget(tasksScrollArea)
        taskListsContainer.setLayout(self.tasksScrollLayout)
        tasksScrollArea.setWidget(taskListsContainer)
        rightLayout.addWidget(tasksScrollArea)
        
        addTaskBtn = QPushButton("+ Add Task")
        addTaskBtn.setCursor(QCursor(Qt.PointingHandCursor))
        addTaskBtn.setStyleSheet(self.taskBtnStyle % (add_task_button, primary_text, add_task_button_hover))
        addTaskBtn.clicked.connect(self.addNewTask)
        rightLayout.addWidget(addTaskBtn)

        self.refreshLists()
        self.refreshTaskList()

    def addNewTask(self):
        self.addTaskCallback(self.selectedList.listData.name)

    def addNewList(self):
        ListManager.create_list()
        self.selectedList = None
        self.refreshLists()

    def removeSelectedList(self):
        ListManager.delete_task_list(self.selectedList.listData.name)
        self.selectedList = None
        self.refreshLists()
        self.refreshTaskList()

    def onListSelected(self, list):
        self.selectedList = list
        self.refreshTaskList()

    def onTaskPin(self, toggle, task:Task):
        ListManager.toggle_task_pin(task.task_id, toggle)
        self.refreshTaskList()

    def onTaskCheck(self, toggle, task:Task):
        ListManager.toggle_task_check(task.task_id, toggle)
        self.refreshTaskList()
    
    def onListPin(self, toggle, taskList: TaskList):
        ListManager.toggle_list_pin(taskList.name, toggle)
        self.refreshLists()

    def refreshLists(self):
        # clear list in reverse
        for i in reversed(range(self.listsScrollLayout.count()-1)): 
            self.listsScrollLayout.itemAt(i).widget().setParent(None)

        sortedLists = ListManager.get_all_lists()
        sortedLists.sort(key=lambda ls: ls.name)
        sortedLists.sort(reverse=True, key=lambda ls: ls.pinned)
        
        #re add lists
        for i in sortedLists:
            listWidget = ListWidget(i)
            if not self.selectedList:
                self.selectedList = listWidget
            listWidget.selected.connect(self.onListSelected)
            listWidget.pinToggled.connect(lambda toggle, i=i: self.onListPin(toggle, i))
            listWidget.nameChanged.connect(lambda new_name, i=i: ListManager.rename_list(i.name, new_name))
            self.listsScrollLayout.insertWidget(self.listsScrollLayout.count() - 1,listWidget) 

        if self.selectedList:
            self.selectedList.ToggleActive()
    
    def refreshTaskList(self):
        if not self.selectedList: return

        # clear list in reverse
        for i in reversed(range(self.tasksScrollLayout.count()-1)): 
            self.tasksScrollLayout.itemAt(i).widget().deleteLater()

        #re add lists
        listName = self.selectedList.listData.name
        tasks = ListManager.get_list(listName).tasks
        if "alphabet" in self.sortBox.currentText().lower():
            tasks.sort(key=lambda task: task.title)
            print("sort alph")
        elif "priority" in self.sortBox.currentText().lower():
            tasks.sort(key=lambda task: task.priority.value)
            print("sort prior")
        elif "deadline" in self.sortBox.currentText().lower():
            tasks.sort(key=lambda task: task.deadline)
            print("sort dead")
        tasks.sort(reverse=True, key=lambda task: task.pinned)
        for i in tasks:
            taskWidget = TaskWidget(i)
            taskWidget.doubleClicked.connect(lambda i=i: self.modifyTaskCallback(i))
            taskWidget.checkToggled.connect(lambda toggle, i=i: self.onTaskCheck(toggle, i))
            taskWidget.pinToggled.connect(lambda toggle, i=i: self.onTaskPin(toggle, i))
            self.tasksScrollLayout.insertWidget(self.tasksScrollLayout.count()-1, taskWidget)


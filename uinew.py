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
from MainView import MainView
from task_list import ListManager

# go kill your self
# database
# add task
# main view
# ui new add tasks callbacks database
# go kill yourself

class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.modifyTaskWidget = None
        self.mainView = MainView(self.viewAddTaskPanel, self.viewModifyTaskPanel)
        self.addWidget(self.mainView)
        self.addWidget(TaskViewPanel("Add New Task", self.addTask, self.closePanel))
        self.setCurrentIndex(0)
        
    def viewAddTaskPanel(self, list_name):
        self.list_name = list_name
        self.setCurrentIndex(1)
    
    def viewModifyTaskPanel(self, task):
        self.modifyTaskWidget = TaskViewPanel("Update Task", self.modifyTask, self.closePanel, self.deleteTask, task)
        self.addWidget(self.modifyTaskWidget)
        self.setCurrentIndex(2)
    
    def addTask(self, task):
        ListManager.add_task(self.list_name, task)
        self.closePanel()
        self.mainView.refreshTaskList()

    def modifyTask(self, task):
        ListManager.update_task(task.task_id, task)
        self.closePanel()
        self.mainView.refreshTaskList()

    # 2024-05-02
    # 
    def deleteTask(self, task):
        ListManager.delete_task(task.task_id)
        self.closePanel()
        self.mainView.refreshTaskList()

    def closePanel(self):
        if self.modifyTaskWidget:
            self.removeWidget(self.modifyTaskWidget)
            self.modifyTaskWidget.deleteLater()
            self.modifyTaskWidget = None
        self.setCurrentIndex(0)

def main():
   app = QApplication(sys.argv)
   ex = MainWindow()
   ex.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
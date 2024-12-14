from PyQt5 import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt5 import *
from PyQt5.QtWidgets import *
from widgets.colors import *
from task_list import *

class TaskViewPanel(QFrame):
    labelStyle = """
    font-family: 'ui-sans-serif';
    font-size: 15px;
    border-style: none;
    padding: 0;
    color: %s;
    """ % primary_text
    
    inputEditStyle = """
    font-family: 'ui-sans-serif';
    font-size: 12px;
    color: %s;
    background-color: #374151;
    padding: 5px;
    """ % primary_text

    btnStyle = """
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

    def __init__(self, title, submitCallback, closeCallback, deleteCallback = None, taskData: Task = None):
        super().__init__()
        self.submitCallback = submitCallback
        self.taskData = taskData

        backgroundLayout = QVBoxLayout()
        backgroundLayout.setAlignment(Qt.AlignHCenter)
        
        self.setLayout(backgroundLayout)
        self.setStyleSheet("QFrame{background-color:%s; padding:40}" % main_bg)
        
        mainLayout = QVBoxLayout()
        mainContainer = QFrame()
        mainContainer.setMaximumWidth(400)
        mainContainer.setLayout(mainLayout)
        mainContainer.setStyleSheet("""
        QFrame{
            background-color: %s;
            padding: 5px;
            border-radius: 5px;
            border-style: solid;
            border-width: 1px;
            border-color: #8d929c;
        }""" %sidebar_bg)
        backgroundLayout.addWidget(mainContainer)

        labelAndExitLayout = QHBoxLayout()
        labelAndExitLayout.setContentsMargins(0,0,0,0)
        labelAndExitLayout.setSpacing(0)
        labelAndExitContainer = QWidget()
        labelAndExitContainer.setLayout(labelAndExitLayout)
        mainLayout.addWidget(labelAndExitContainer)

        mainLabel = QLabel(title)
        mainLabel.setStyleSheet("border-style: none;font-family: ui-sans-serif; font-weight:bold; font-size:22px; color: %s" % primary_text)
        labelAndExitLayout.addWidget(mainLabel)
        labelAndExitLayout.addStretch()

        closeBtn = QPushButton()
        closeBtn.setIcon(QIcon('icons/x.svg'))
        closeBtn.setStyleSheet("""
        QPushButton{
            background-color: rgba(0,0,0,0);
            padding: 3px;
        }
        
        QPushButton:hover{
            background-color: rgba(0,0,0,0.15);
        }
        """)
        closeBtn.setCursor(QCursor(Qt.PointingHandCursor))
        closeBtn.clicked.connect(closeCallback)
        labelAndExitLayout.addWidget(closeBtn)

        formLayout = QVBoxLayout()
        formContainer = QWidget()
        formContainer.setLayout(formLayout)
        mainLayout.addWidget(formContainer)

        nameLabel = QLabel("Name")
        nameLabel.setStyleSheet(self.labelStyle)
        self.nameInput = QLineEdit()
        self.nameInput.setStyleSheet(self.inputEditStyle) 
        descriptionLabel = QLabel("Description")
        descriptionLabel.setStyleSheet(self.labelStyle)
        self.descriptionInput = QTextEdit()
        self.descriptionInput.setStyleSheet(self.inputEditStyle) 
        deadlineLabel = QLabel("Deadline")
        deadlineLabel.setStyleSheet(self.labelStyle)  
        self.deadlineInput = QDateEdit()
        self.deadlineInput.setStyleSheet("""
        QDateEdit{
        color:  %s;
        border-color: #8d929c;
        border-style: solid;
        background-color: #374151;
        padding: 5px;
        }
        """ % (primary_text))
        self.deadlineInput.setDate(QDate.currentDate())  
        priorityLabel = QLabel("Priority")
        priorityLabel.setStyleSheet(self.labelStyle)
        self.priorityInput = QComboBox()
        self.priorityInput.addItems(['High', 'Medium', 'Low'])
        self.priorityInput.setStyleSheet("color:%s;padding:5px; background-color: #374151;" % (primary_text))

        formLayout.addWidget(nameLabel)
        formLayout.addWidget(self.nameInput)
        formLayout.addWidget(descriptionLabel)
        formLayout.addWidget(self.descriptionInput)
        formLayout.addWidget(deadlineLabel)
        formLayout.addWidget(self.deadlineInput)
        formLayout.addWidget(priorityLabel)
        formLayout.addWidget(self.priorityInput)

        submitBtn = QPushButton("Done!")
        submitBtn.setStyleSheet(self.btnStyle % (add_task_button, primary_text, add_task_button_hover))
        submitBtn.setCursor(QCursor(Qt.PointingHandCursor))
        submitBtn.clicked.connect(self.submit)
        mainLayout.addWidget(submitBtn)

        if deleteCallback:
            deleteBtn = QPushButton("Delete.")
            deleteBtn.setStyleSheet(self.btnStyle % (delete_list_button, primary_text, delete_list_button_hover))
            deleteBtn.setCursor(QCursor(Qt.PointingHandCursor))
            deleteBtn.clicked.connect(lambda: deleteCallback(taskData))
            mainLayout.addWidget(deleteBtn)
            

        if taskData:
            self.nameInput.setText(taskData.title)
            self.descriptionInput.setText(taskData.description)
            date = taskData.deadline
            self.deadlineInput.setDate(QDate(date.year, date.month, date.day))
            self.priorityInput.setCurrentText(taskData.priority.name)        
            
    def submit(self):
        date = self.deadlineInput.date()
        pyDate = datetime(date.year(), date.month(), date.day())
        self.submitCallback(Task( self.taskData.task_id if self.taskData else 0, self.nameInput.text(), self.descriptionInput.toPlainText(), pyDate, Priority[self.priorityInput.currentText()], False, False))
        self.nameInput.setText('')
        self.descriptionInput.setText('')

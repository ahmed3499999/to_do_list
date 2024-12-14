from PyQt5 import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt5 import *
from PyQt5.QtWidgets import *
from .colors import *
from .PinButton import PinButton
from task_list import *

class TaskWidget(QFrame):
    checkedStyle = "text-decoration:line-through; font-weight: italic; color: %s;" % muted_text
    uncheckedStyle = "color: %s;" % secondary_text
    doubleClicked = pyqtSignal()
    checkToggled = pyqtSignal()
    pinToggled = pyqtSignal()
    labelStyle = """
            margin-right:10;
            padding:0;
            font-family: 'ui-sans-serif';
            font-size: 18px;
            %s;
            """
    
    def __init__(self, taskData: Task, parent = None):
        super().__init__(parent)
        self.setStyleSheet(" background-color: '%s';border-radius: 3px;" % sidebar_bg) 
        self.setFixedHeight(50)
        self.taskData = taskData
        
        priorityIcon = QLabel()
        priority = taskData.priority.value
        icon = 'red_circle.svg' if priority == 0 else 'yellow_circle.svg' if priority == 1 else 'green_circle' 
        priorityIcon.setPixmap(QPixmap('icons/' + icon).scaled(10,10, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation))
        priorityIcon.setStyleSheet('margin-left: 13px')

        self.checkBox = QCheckBox()
        print(taskData.checked, "HELLO PEPOPLE")
        self.checkBox.setStyleSheet("""
            QCheckBox{
                padding-top:10;                        
                padding-bottom:10;
                margin-left: 13px;                        
            }
            QCheckBox::indicator:unchecked {
                image: url(icons/circle.svg);
            }

            QCheckBox::indicator:checked {
            image: url(icons/check.svg);
            }
        """)
        self.checkBox.stateChanged.connect(self.ToggleActivity)
        self.checkToggled = self.checkBox.stateChanged

        self.titleLabel = QLabel(taskData.title)
        self.titleLabel.setStyleSheet(self.labelStyle % self.checkedStyle )

        dateIcon = QLabel()
        dateIcon.setPixmap(QPixmap('icons/calendar.svg').scaled(20,20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation))

        dateLabel = QLabel(taskData.deadline.strftime('%Y-%m-%d'))
        dateLabel.setStyleSheet("color: %s;font-family:'ui-sans-serif'; font-size: 13px;margin-left: 10px;" % muted_text)

        pinButton = PinButton()
        if taskData.pinned: pinButton.toggleIcon()
        self.pinToggled = pinButton.pinToggled

        mainLayout = QHBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)  
        mainLayout.setSpacing(0)  

        mainLayout.addWidget(priorityIcon)
        mainLayout.addWidget(self.checkBox)
        mainLayout.addWidget(self.titleLabel)
        mainLayout.addStretch()
        mainLayout.addWidget(dateIcon)
        mainLayout.addWidget(dateLabel)
        mainLayout.addWidget(pinButton)
        mainLayout.addSpacing(20)

        self.ToggleActivity(taskData.checked)
        self.setLayout(mainLayout)

    def ToggleActivity(self, toggle):
        self.titleLabel.setStyleSheet(self.labelStyle % (self.checkedStyle if toggle else self.uncheckedStyle))
        self.checkBox.setChecked(toggle)

    def mouseDoubleClickEvent(self, a0):
        super().mouseDoubleClickEvent(a0)
        self.doubleClicked.emit()
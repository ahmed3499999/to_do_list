from PyQt5 import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt5 import *
from PyQt5.QtWidgets import *
from .colors import *
from .PinButton import PinButton

class TaskWidget(QFrame):
    checkedStyle = "text-decoration:line-through; font-weight: italic; color: %s;" % muted_text
    uncheckedStyle = "color: %s;" % secondary_text
    def __init__(self, title, date, toggle, parent = None):
        super().__init__(parent)
        self.setStyleSheet(" background-color: '%s';border-radius: 3px;" % sidebar_bg) 
        self.setFixedHeight(50)
        
        priorityIcon = QLabel()
        priorityIcon.setPixmap(QPixmap('icons/circle_fill.svg').scaled(10,10, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation))
        priorityIcon.setStyleSheet('margin-left: 13px')

        checkBox = QCheckBox()
        checkBox.setStyleSheet("""
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
        checkBox.setChecked(toggle)

        titleLabel = QLabel(title)
        titleLabel.setStyleSheet("""
            margin-right:10;
            padding:0;
            font-family: 'ui-sans-serif';
            font-size: 18px;
            %s;
            """ % ((self.checkedStyle if toggle else self.uncheckedStyle)))

        dateIcon = QLabel()
        dateIcon.setPixmap(QPixmap('icons/calendar.svg').scaled(20,20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation))

        dateLabel = QLabel(date)
        dateLabel.setStyleSheet("color: %s;font-family:'ui-sans-serif'; font-size: 13px;margin-left: 10px;" % muted_text)

        pinButton = PinButton()

        mainLayout = QHBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)  
        mainLayout.setSpacing(0)  

        mainLayout.addWidget(priorityIcon)
        mainLayout.addWidget(checkBox)
        mainLayout.addWidget(titleLabel)
        mainLayout.addStretch()
        mainLayout.addWidget(dateIcon)
        mainLayout.addWidget(dateLabel)
        mainLayout.addWidget(pinButton)
        mainLayout.addSpacing(20)

        self.setLayout(mainLayout)
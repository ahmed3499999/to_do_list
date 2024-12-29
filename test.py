import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from widgets.colors import *
import mysql.connector
from accounts import AccManager
from widgets.colors import *

app = QApplication(sys.argv)
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Task List Login')
        self.setFixedSize(400, 300)
        self.setStyleSheet(f"background-color: {BACKGROUND_COLOR}")
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Title
        title_label = QLabel('Task List')
        title_label.setFont(QFont('Arial', 24, QFont.Bold))
        title_label.setStyleSheet(f"color: {PRIMARY_COLOR}")
        title_label.setAlignment(Qt.AlignCenter)
        
        # Email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Email')
        self.email_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 10px;
                border: 2px solid {SECONDARY_COLOR};
                border-radius: 5px;
                background-color: white;
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 2px solid {PRIMARY_COLOR};
            }}
        """)
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.email_input.styleSheet())
        
        # Login button
        login_button = QPushButton('Login')
        login_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY_COLOR};
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {SECONDARY_COLOR};
            }}
        """)
        login_button.clicked.connect(self.login)
        
        # Register button
        register_button = QPushButton('Register')
        register_button.setStyleSheet(login_button.styleSheet())
        register_button.clicked.connect(self.register)
        
        # Google login button
        google_button = QPushButton('Login with Google')
        google_button.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                color: black;
                padding: 10px;
                border: 2px solid {SECONDARY_COLOR};
                border-radius: 5px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #f0f0f0;
            }}
        """)
        google_button.clicked.connect(self.google_login)
        
        # Add widgets to layout
        main_layout.addWidget(title_label)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.email_input)
        main_layout.addWidget(self.password_input)
        main_layout.addWidget(login_button)
        main_layout.addWidget(register_button)
        main_layout.addWidget(google_button)
        
        self.setLayout(main_layout)
        
    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()
        if not email or not password:
            QMessageBox.warning(self,"error", "Please insert an email and password")
            return
        
        if AccManager.login_email(email, password):
            self.open_main_window()
        else:
            QMessageBox.warning(self,"error", "Incorrect user or password")

    def register(self):
        email = self.email_input.text()
        password = self.password_input.text()
        
        if AccManager.register_email(email, password):
            self.open_main_window()
        else:
            QMessageBox.warning(self,"error", "Email already exists")
        
    def google_login(self):
        AccManager.register_google()
        self.open_main_window()
    
    def open_main_window(self):
        global app
        global login_window
        login_window.hide()
        from uinew import main as start_todo
        start_todo(app)

login_window = LoginWindow()
def main():
    if AccManager.is_logged_in():
        login_window.open_main_window()
    else:
        login_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

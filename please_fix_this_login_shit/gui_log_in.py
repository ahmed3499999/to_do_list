import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
import goolge_log_in
import account_manager as account_manager
# import database 
class LogIn(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the .ui file
        uic.loadUi("gui1.ui", self)
        
        # self.ERROR_LABEL.setStyleSheet("QLabel{color:'red'}",)
        # Connect GUI elements to their respective functions
        self.login.clicked.connect(self.log_in_normal)
        self.google.clicked.connect(self.log_in_google)
    def log_in_normal(self):
        # Get the entered username and password
        email = self.username.text().strip()
        password = self.password.text().strip()
        if email is None or password is None:
            
            msg= 'Account not found'
            self.ui.ERROR_LABEL.setText(msg)
            self.ERROR_LABEL.setStyleSheet("QLabel{color:'red'}")
            LogIn()
            
             
        
        return_login_task_list=account_manager.AccManager(email,password)
        if return_login_task_list=='Account not found':
            msg= 'Account not found'
            self.ERROR_LABEL.setText(msg)
            self.ERROR_LABEL.setStyleSheet("QLabel{color:'red'}")
        if return_login_task_list=='Passwords do not match':
            msg= 'Passwords do not match'
            self.ERROR_LABEL.setText(msg)
            self.ERROR_LABEL.setStyleSheet("QLabel{color:'red'}")
        if return_login_task_list=='This account is logged in through google account':
            msg= 'This account is logged in through google account'
            self.ERROR_LABEL.setText(msg)
            self.ERROR_LABEL.setStyleSheet("QLabel{color:'red'}")
            
    def log_in_google(self):
        goolge_log_in.authenticate()
        goolge_log_in.log_in()
class sign_up(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the .ui file
        uic.loadUi("gui_sign_up.ui", self)
        # Connect GUI elements to their respective functions
        self.signup.clicked.connect(self.sign_up_normal)
        self.google.clicked.connect(self.sign_up_google)
    def sign_up_normal(self):
        # Get the entered username and password
        username = self.email.text().strip()
        password = self.spassword.text().strip()
        password = self.cs_password.text().strip()
    def sign_up_google(self):
        goolge_log_in.authenticate()
        goolge_log_in.log_in()
       



def main():
    def transition_to_sign_up():
        logInWindow.hide()
        signUpWindow.show()
    def transition_to_log_in():
        signUpWindow.hide()
        logInWindow.show()
    app = QtWidgets.QApplication(sys.argv)
    logInWindow = LogIn()
    signUpWindow = sign_up()
    logInWindow.show()
    logInWindow.signup_button.clicked.connect(transition_to_sign_up)
    signUpWindow.Back_to_log_in.clicked.connect(transition_to_log_in)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


        

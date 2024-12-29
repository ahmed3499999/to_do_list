import os
import database as db
from googleauth import authenticate

creds_file = 'creds.txt'
class AccManager:
    def register_google():
        global creds_file
        data = authenticate()
        if AccManager.email_exists(data[1]):
            with open(creds_file, 'w') as f:
                f.write('\n'.join(['0' ,data[1], data[0]]))
        else:
            db.add_google_id(data[0], data[1])
            
        db.user_id = db.login_google(data[1])
    
    def register_email(email, password):
        global creds_file
        if db.email_exist(email): return False
        db.add_email(email, password)
        with open(creds_file, 'w') as f:
            f.write('\n'.join(['1',email,password]))

        db.user_id = db.login_email(email, password)
        return True

    def login_email(email, password):
        if not db.email_exist(email): return False
        if not db.login_email(email, password): return False
        db.user_id = db.login_email(email, password)
        return True
    
    def is_logged_in():
        global creds_file
        if os.path.exists(creds_file):
            with open(creds_file, 'r') as f:
                data = f.readlines()
                if data[0] == '0':
                    db.user_id = db.login_google(data[2])
                elif data[0] == '1':
                    db.user_id = db.login_email(data[1], data[2])
        else:
            return False


    def email_exists(email):
        return db.email_exist(email)
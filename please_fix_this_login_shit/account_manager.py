from datetime import datetime
import os
class Acc:
    def __init__(self, open_id, user_id, email, password):
        self.open_id = open_id
        self.user_id = user_id
        self.email = email
        self.password = password
class AccManager:
    @staticmethod
    def get_acc(email: str) -> Acc:
        pass

    @staticmethod
    def login(email: str, password: str) -> str:
        if email is None or password is None:
            return 'Empty inputs'
        acc = AccManager.get_acc(email)
        if acc is None:
            return 'Account not found'
        if acc.password != password:
            return 'Passwords do not match'
        if acc.open_id is not None and acc.password is not None:
            return 'This account is logged in through google account'
        f = open('log.txt', 'w')
        f.write(acc.user_id)
        return ''

    @staticmethod
    def sign_up(email: str, password: str, repeat_password: str) -> str:
        if email is None or password is None:
            return 'Empty input'
        if AccManager.get_acc(email) is not None:
            return 'Account already exists'
        if len(password) < 8:
            return 'Passwords must have at least 8 characters'
        if password != repeat_password:
            return 'Passwords do not match'
        # Database must update user_id
        f = open('log.txt', 'w')
        # f.write(user_id)
        return ''

    @staticmethod
    def logout() -> None:
        if os.path.exists('log.txt'):
            os.remove('log.txt')
            print(f"{'log.txt'} has been deleted.")
        else:
            print(f"{'log.txt'} does not exist.")
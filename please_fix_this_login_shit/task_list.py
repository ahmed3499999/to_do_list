from datetime import datetime
import os
# class Acc:
#     def __init__(self, open_id, user_id, email, password):
#         self.open_id = open_id
#         self.user_id = user_id
#         self.email = email
#         self.password = password

# this class only functions as a way to store the task data, it should not have any logical functionality
class Task:
    def __init__(self, title: str, date: datetime, important: bool, description: str = None,
                  pinned: bool = False) -> None:
        self.title = title
        self.description = description
        self.date = date
        self.pinned = pinned
        self.important = important

# task list instances serve no functionality and are used as a datastructures for passing data around
# do not manipulate it directly, instead use ListManager functions
# do not create task list objects directly, instead use create_list
class TaskList:
    def __init__(self, name: str, tasks: list[Task], pinned: bool = False) -> None:
        self.name = name
        self.tasks = tasks
        self.pinned = pinned

# task lists are unique by name, this class will handle updating the task lists by name using static methods
# all calls for the database handling for tasks and task lists occurs in this class,
# direct database queries should be kept in a separate file
class ListManager:
    # checks if the list name is unique then initialize a new list with no tasks
    @staticmethod
    def create_list(list_name: str) -> TaskList:
        if ListManager.search_list(list_name) is not None:
            return None
        new_list = TaskList(list_name, [])
        #TODO database update
        return new_list

    # checks if there is a list with this name and then rename it
    @staticmethod
    def rename_list(name: str, new_name: str) -> None:
        if (ListManager.search_list(name) is None) or (ListManager.search_list(new_name) is not None):
            return None
        list_to_update = ListManager.get_list(name)
        list_to_update.name = new_name
        #TODO database update

    @staticmethod
    def get_list(list_name: str) -> TaskList:
        #TODO database retrieval
        pass

    @staticmethod
    def get_all_lists() -> list[TaskList]:
        #TODO database retrieval
        pass

    # checks if there is a list with this name and then pin it
    @staticmethod
    def pin_list(list_name: str) -> TaskList:
        if ListManager.search_list(list_name) is None:
            return None
        list_to_pin = ListManager.get_list(list_name)
        list_to_pin.pinned = True
        #TODO database update
        return list_to_pin

    @staticmethod
    def search_list(list_name: str) -> TaskList:
        if ListManager.get_list(list_name) is None:
            print("List name is incorrect or unavailable")
            return None
        return ListManager.get_list(list_name)

    @staticmethod
    def delete_task_list(list_name: str) -> TaskList:
        #TODO database query for deletion
        pass

    # checks if there is a list with this name and the task name is unique and then add a new task to the list with only properties passed as keyword arguments
    @staticmethod
    def add_task(list_name: str, **kwargs) -> Task:
        if ListManager.search_task(list_name, kwargs['title']) is not None:
            return None
        new_task = Task(**kwargs)
        ListManager.get_list(list_name).tasks.append(new_task)
        #TODO database update
        return new_task

    # checks if there is a list and a task with this name and then only update the attributes passed as keyword arguments
    @staticmethod
    def update_task(list_name: str, **kwargs) -> None:
        task = ListManager.search_task(list_name, kwargs['title'])
        if task is None:
            return None
        for key, value in kwargs.items():
            setattr(task, key, value)
        #TODO database update

    # checks if there is a list and a task with these names and then pin it
    @staticmethod
    def pin_task(list_name: str, task_name: str) -> Task:
        task = ListManager.search_task(list_name, task_name)
        if task is None:
            return None
        task.pinned = True
        return task
        #TODO database update

    # checks if there is a list with this name and then sorted alphabetically
    @staticmethod
    def sort_tasks_alpha(list_name: str) -> TaskList:
        lst = ListManager.search_list(list_name)
        if lst is None:
            return None
        lst.tasks.sort()
        return lst

    # checks if there is a list with this name and then sorted based on importance
    @staticmethod
    def sort_tasks(list_name: str) -> TaskList:
        #TODO database retrieval
        lst = ListManager.search_list(list_name)
        if lst is None:
            return None
        lst1 = []
        lst2 = []
        for task in lst.tasks:
            if task.important:
                lst1.append(task)
            else:
                lst2.append(task)
        lst.tasks = lst1.extend(lst2)
        return lst

    @staticmethod
    def search_task(list_name: str, task_name: str) -> Task:
        if ListManager.search_list(list_name) is None:
            return None
        for task in ListManager.get_list(list_name).tasks:
            if task.title == task_name:
                return task
        print("Task name is incorrect or unavailable")
        return None

    @staticmethod
    def delete_task(list_name: str, task_name: str) -> Task:
        #TODO database query for deletion
        pass

# class AccManager:
#     @staticmethod
#     def get_acc(email: str) -> Acc:
#         pass

#     @staticmethod
#     def login(email: str, password: str) -> str:
#         if email is None or password is None:
#             return 'Empty inputs'
#         acc = AccManager.get_acc(email)
#         if acc is None:
#             return 'Account not found'
#         if acc.password != password:
#             return 'Passwords do not match'
#         if acc.open_id is not None and acc.password is not None:
#             return 'This account is logged in through google account'
#         f = open('log.txt', 'w')
#         f.write(acc.user_id)
#         return ''

#     @staticmethod
#     def sign_up(email: str, password: str, repeat_password: str) -> str:
#         if email is None or password is None:
#             return 'Empty input'
#         if AccManager.get_acc(email) is not None:
#             return 'Account already exists'
#         if len(password) < 8:
#             return 'Passwords must have at least 8 characters'
#         if password != repeat_password:
#             return 'Passwords do not match'
#         # Database must update user_id
#         f = open('log.txt', 'w')
#         # f.write(user_id)
#         return ''

#     @staticmethod
#     def logout() -> None:
#         if os.path.exists('log.txt'):
#             os.remove('log.txt')
#             print(f"{'log.txt'} has been deleted.")
#         else:
#             print(f"{'log.txt'} does not exist.")
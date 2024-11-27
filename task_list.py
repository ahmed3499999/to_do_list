from datetime import datetime
from database import *
from typing import List # for statically typed lists

# this class only functions as a way to store the task data, it should not have any logical functionality 
class Task:
    def __init__(self, title: str, describtion: str = None, date: datetime = datetime.now(), 
                    pinned: bool = False, important: bool = False) -> None:
        self.title = title
        self.description = describtion
        self.date = date
        self.pinned = pinned
        self.important = important

# task list instances serve no functionality and are used as a datastructures for passing data around
# do not manipulate it directly, instead use ListManager functions
# do not create task list objects directly, instead use create_list
class TaskList:
    def __init__(self, name: str, tasks: List[Task], pinned: bool = False) -> None:
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

        #TODO database update

    @staticmethod
    def get_list(list_name: str) -> TaskList:
        #WARNING the order of tuple task is important
        tasks = [Task(*task) for task in get_tasks()]
        return TaskList('', tasks, False)
        pass

    @staticmethod
    def get_all_lists() -> List[TaskList]:
        #TODO database retrieval
        pass

    # checks if there is a list with this name and then pin it
    @staticmethod
    def pin_list(list_name: str) -> None:
        if ListManager.search_list(list_name) is None:
            return None
        #TODO database update

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
    def add_task(list_name: str, **kwargs) -> None:
        #TODO MAKE IT SO NO DUPES OF TASKS ARE MADE
        # if ListManager.search_task(list_name, kwargs['title']) is not None:
        #     return None
        add_task('', **kwargs)

    # checks if there is a list and a task with this name and then only update the attributes passed as keyword arguments
    @staticmethod
    def update_task(list_name: str, **kwargs) -> None:
        task = ListManager.search_task(list_name, kwargs['title'])
        if task is None:
            return None
        
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
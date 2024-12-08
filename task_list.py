from datetime import date
from database import *
from typing import List # for statically typed lists
from enum import Enum

#enums for easy conversion between string and int 
class Priority(Enum):
    high = 0
    medium = 1
    low = 2

class Repeat(Enum):
    none = 0
    daily = 1
    weekly = 2
    monthly = 3
    yearly = 4

# this class only functions as a way to store the task data, it should not have any logical functionality 
# priority(HIGH, MEDIUM, LOW) = (0,1,2)
# repeatness(none,daily,weekly,monthly,yearly) = (0,1,2,3,4)
class Task:
    def __init__(self, title: str, description: str = None, deadline: date = date.today(),
                 priority: int = 2, repeatness: int = 0) -> None:
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.repeatness = repeatness

# this class handles tasks using static methods
# all calls for the database handling for tasks occur in this class,
# direct database queries should be kept in a separate file
class TaskManager:
    @staticmethod
    def add_task(**kwargs) -> None:
        if TaskManager.task_exists(kwargs['title']): return

        add_task(**kwargs)

    @staticmethod
    def update_task(current_title, **kwargs) -> None:
        if TaskManager.task_exists(current_title): return
        
        update_task(current_title, **kwargs)
    
    @staticmethod
    def get_all_tasks() -> List[Task]:
        # loop over every task and use it to create a new Task object
        # this is called list comprehension
        return [Task(*task) for task in get_tasks()]

    @staticmethod
    def task_exists(title: str) -> bool:
        # loop over every task and get its title
        titles = [task.title for task in TaskManager.get_all_tasks()]
        return title in titles
    
    @staticmethod
    def delete_task(title: str) -> None:
        if not TaskManager.task_exists(title): return

        delete_task(title)
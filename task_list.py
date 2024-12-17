from datetime import datetime
import os
from enum import Enum
from typing import List
import database as db

class Priority(Enum):
    High = 0
    Medium = 1
    Low = 2

# this class only functions as a way to store the task data, it should not have any logical functionality
class Task:
    def __init__(self,task_id: int, title: str, description: str, deadline: datetime, priority: Priority, pinned: bool, checked: bool) -> None:
        self.task_id = task_id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.pinned = pinned
        self.checked = checked

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
    def create_list() -> None:
        new_index = 1
        listExist = False
        while True:
            for i in ListManager.get_all_lists():
                if i.name == ("New List " + str(new_index)):
                    listExist = True

            if listExist:
                new_index += 1
                listExist = False
            else:
                db.add_list("New List " + str(new_index))
                break
        

    # checks if there is a list with this name and then rename it
    @staticmethod
    def rename_list(name: str, new_name: str) -> None:
        if (ListManager.search_list(name) is None) or (ListManager.search_list(new_name) is not None):
            return None
        list_to_update = ListManager.get_list(name)
        list_to_update.name = new_name
        # TODO database update

    @staticmethod
    def get_list(list_name: str) -> TaskList:
        for i in ListManager.get_all_lists():
            if i.name == list_name.strip():
                return i
            
        return None

    @staticmethod
    def get_all_lists() -> List[TaskList]:
        result = []
        tasks = []
        for i in db.get_user_lists():
            if i[0]:
                for x in i[0].strip().split(','):
                    if x:
                        tasks.append(ListManager.get_task(x))
            else:
                tasks = []
            result.append(TaskList(i[1], tasks, i[2]))
            tasks = []

        return result

    @staticmethod
    def delete_task_list(list_name: str) -> TaskList:
        db.delete_list(list_name)
    
    @staticmethod
    def rename_list(list_name:str, new_name: str) -> None:
        print("renaming")
        db.update_list(list_name, title=new_name)

    @staticmethod
    def toggle_list_pin(list_name: str, toggle: bool) -> None:
        db.update_list(list_name, pinned=toggle)

    @staticmethod
    def get_task(task_id: int):
        taskData = db.get_task(task_id)
        #task_id title description deadline priority pinned checked
        return Task(task_id, taskData[1], taskData[2], taskData[3], Priority(taskData[4]), taskData[5], taskData[6])

    # checks if there is a list with this name and the task name is unique and then add a new task to the list with only properties passed as keyword arguments
    @staticmethod
    def add_task(list_name: str, task: Task):
        db.add_task(list_name, title=task.title, description=task.description, deadline=task.deadline, priority=task.priority.value)

    # checks if there is a list and a task with this name and then only update the attributes passed as keyword arguments
    @staticmethod
    def update_task(task_id: int, task: Task) -> None:
        print ("we got ", task.priority.value)
        db.update_task(task_id, title=task.title, description=task.description, deadline=task.deadline, priority=task.priority.value)

    @staticmethod
    def toggle_task_check(task_id: int, toggle: bool) -> None:
        db.update_task(task_id, checked= True if toggle else False)
    
    @staticmethod
    def toggle_task_pin(task_id: int, toggle: bool) -> None:
        db.update_task(task_id, pinned=toggle)

    @staticmethod
    def delete_task(task_id) -> Task:
        for ls in ListManager.get_all_lists():
            tasks = [task.task_id for task in ls.tasks]
            print("removed shit1", tasks)
            if task_id in tasks:
                tasks.remove(task_id)
                print("removed shit", tasks)
                db.update_list(ls.name, task_ids=','.join(tasks) if tasks else ' ')
                return
        
        db.delete_task(task_id)
  
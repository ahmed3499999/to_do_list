from datetime import datetime

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

    # checks if there is a list with this name and then sorted based on Eisenhower matrix
    @staticmethod
    def sort_tasks(list_name: str, deadline: datetime) -> TaskList:
        #TODO database retrieval
        lst = ListManager.search_list(list_name)
        if lst is None:
            return None

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
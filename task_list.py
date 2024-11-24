from datetime import datetime

# this class only functions as a way to store the task data, it should not have any logical functionality 
class Task:
    def __init__(self, id: int, title: str, description: str = None, date: datetime = None,
                  pinned: bool = False, important: bool = False) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.date = date
        self.pinned = pinned
        self.important = important

# task list instances serve no functionality and are used as a datastructure for passing data around
# do not manipulate it directly, instead use ListManager functions
# do not create task list objects directly, instead use create_list
class TaskList:
    def __init__(self, name: str, pinned: bool, tasks: list[Task]) -> None:
        self.name = name
        self.pinned = pinned
        self.tasks = tasks

# task lists are unique by name, this class will handle updating the task lists by name using static methods
# all calls for the database handling for tasks and task lists occurs in this class,
# direct database queries should be kept in a separate file
class ListManager:
    @staticmethod
    def create_list(name: str, pinned: bool) -> None:
        newList = TaskList(name, pinned)
        
        #TODO database call

    @staticmethod
    def update_list(name: str, **kwargs) -> None:
        #TODO databse update
        pass

    @staticmethod
    def update_task(listName: str, taskId: int, **attr) -> None:
        #TODO database update
        pass

    @staticmethod
    def get_list(listName: str) -> TaskList:
        #TODO database retrieval
        pass
    
    @staticmethod
    def get_all_lists() -> list[TaskList]:
        #TODO database retrieval
        pass

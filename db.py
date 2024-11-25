import sqlite3 as db
from task_list import Task, TaskList

f = db.connect("data.db")
a = f.cursor()

def init_db():
    sql = """CREATE TABLE task_lists (
            list_name VARCHAR(255) NOT NULL,
            is_pinned BOOLEAN DEFAULT FALSE
        );
        CREATE TABLE task_list_tasks (
            list_id INT,
            task_id INT,
            PRIMARY KEY (list_id, task_id),
            FOREIGN KEY (list_id) REFERENCES task_lists(list_id) ON DELETE CASCADE,
            FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
        );"""
    
    a.executescript(sql)

def insert_task_list(list_name, is_pinned=False):
    sql = f"INSERT INTO task_lists VALUES (?, ?)"
    a.execute(sql, (list_name, is_pinned))

def insert_task_into_list(list_id, task_id):
    sql = "INSERT INTO task_list_tasks (list_id, task_id) VALUES (%s, %s)"
    a.execute(sql % (list_id, task_id))

insert_task_list("shiekhaaa")

a.execute("SELECT * FROM task_lists")
print(a.fetchmany(5))
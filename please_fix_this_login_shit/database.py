import mysql.connector
from typing import List # for statically typed lists
import random
# Connect to MySQL
connct = mysql.connector.connect(
    host='127.0.0.1',
    passwd='seif2004',
    user='omar2',
    # auth_plugin='mysql_native_password'
)
cursor = connct.cursor()

cursor.execute("USE to_do")
print ("done")
def create_list(name: str) -> None:
    cursor.execute("INSERT INTO list (name, is_pinned) VALUES (%s, false)", name)
    connct.commit()  

def add_task(list_name: str, title, **kwargs) -> None:
    
    cursor.execute("INSERT INTO tasks (title) VALUES (%s);", (title,))    
    update_task(title, **kwargs)
    
    connct.commit()
    
def update_task(task_id: str,**kwargs) -> None:
    cursor.execute("SET SQL_SAFE_UPDATES = 0;")

    if 'title' in kwargs:
        print(type(kwargs['title']))
        cursor.execute("UPDATE tasks SET title=%s WHERE task_id=%s;", (kwargs['title'], task_id))
        connct.commit()
        
    if 'describtion' in kwargs:
            data=kwargs['describtion']
            cursor.execute("UPDATE tasks SET describtion=%s where task_id=%s  ;", (data,task_id))
            connct.commit()
        
    if 'task_date' in kwargs:
            data=kwargs['task_date']
            cursor.execute("UPDATE tasks SET task_date=%s where task_id=%s  ;", (data,task_id))
            connct.commit()
    if 'pinned' in kwargs:
            data=kwargs['pinned']
            cursor.execute("UPDATE tasks SET is_pinned=%s where task_id=%s;", (data,task_id))
            connct.commit()
            
         
    if 'is_important' in kwargs:
            data=kwargs['is_important']
            cursor.execute("UPDATE tasks SET is_important=%s where task_id=%s  ;", (data,task_id))
            connct.commit()

def delete_task(task_id) -> None:
    cursor.execute("DELETE FROM tasks WHERE task_id=%s;",(task_id,))
    print("done deleting task ")
    connct.commit()

def get_tasks(task_id) -> List[tuple]:
    cursor.execute("select * from tasks where task_id=%s",(task_id,))
    return cursor.fetchall()            

def show_list_to_user (user_id):
    cursor.execute("select * from lists where user_id= %s",(user_id,))
    result=cursor.fetchall()
    return (result)


def add_email(email,password):
    cursor.execute("insert into google (email,pass) values (%s,%s)",(email,password))
    connct.commit()
    print("done")
def add_google_id(google_id,email):
    cursor.execute("insert into google (google_id,email) values (%s,%s)",(google_id,email))
    connct.commit()
    print("done")
    
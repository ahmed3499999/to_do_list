import mysql.connector
from typing import List # for statically typed lists
# Connect to MySQL
connct = mysql.connector.connect(
    host='localhost',
    passwd='12345',
    user='root',auth_plugin='mysql_native_password'
)
cursor = connct.cursor()

cursor.execute("USE to_do")

def add_task(title,**kwargs) -> None:
    
    cursor.execute("INSERT INTO tasks (title) VALUES (%s);", (title,))    
    update_task(title, **kwargs)
    
    connct.commit()
    
def update_task(current_title: str,**kwargs) -> None:
    cursor.execute("SET SQL_SAFE_UPDATES = 0;")

    if 'title' in kwargs:
        cursor.execute("UPDATE tasks SET title=%s WHERE title=%s;", (kwargs['title'], current_title))
        connct.commit()
        
    if 'description' in kwargs:
        cursor.execute("UPDATE tasks SET description=%s where title=%s  ;", (kwargs['description'],current_title))
        connct.commit()
        
    if 'deadline' in kwargs:
        cursor.execute("UPDATE tasks SET deadline=%s where title=%s  ;", (kwargs['deadline'],current_title))
        connct.commit()
    
    if 'priority' in kwargs:
        cursor.execute("UPDATE tasks SET priority=%s where title=%s  ;", (kwargs['priority'],current_title))
        connct.commit()
    if 'repeatness' in kwargs:
        cursor.execute("UPDATE tasks SET repeatness=%s where title=%s  ;", (kwargs['repeatness'],current_title))
        connct.commit()

def delete_task(title: str) -> None:
    cursor.execute("DELETE FROM tasks WHERE title=%s;",(title,))
    connct.commit()

def get_tasks() -> List[tuple]:
    cursor.execute("SELECT * FROM tasks")
    return cursor.fetchall()            



# add_task('', title="aaa")
# add_task('', title="bbb")
# print(get_tasks())
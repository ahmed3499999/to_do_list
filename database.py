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

# def create_list(name: str) -> None:

    
#     sql = "INSERT INTO list (name, is_pinned) VALUES (%s, %s)"
#     values = (name, pinned)
#     cursor.execute(sql, values)
#     connct.commit()  
# Call the function
# create_list("run", 1)
  
def add_task(list_name: str, title, **kwargs) -> None:
    
    cursor.execute("INSERT INTO tasks (title) VALUES (%s);", (title,))    
    update_task(title, **kwargs)
    
    connct.commit()
    
def update_task(old_title: str,**kwargs) -> None:
    cursor.execute("SET SQL_SAFE_UPDATES = 0;")

    if 'title' in kwargs:
        print(type(kwargs['title']))
        cursor.execute("UPDATE tasks SET title=%s WHERE title=%s;", (kwargs['title'], old_title))
        connct.commit()
        
    if 'describtion' in kwargs:
            data=kwargs['describtion']
            cursor.execute("UPDATE tasks SET describtion=%s where title=%s  ;", (data,old_title))
            connct.commit()
        
    if 'task_date' in kwargs:
            data=kwargs['task_date']
            cursor.execute("UPDATE tasks SET task_date=%s where title=%s  ;", (data,old_title))
            connct.commit()
    if 'pinned' in kwargs:
            data=kwargs['pinned']
            cursor.execute("UPDATE tasks SET is_pinned=%s where title=%s;", (data,old_title))
            connct.commit()
            
            
    if 'is_important' in kwargs:
            data=kwargs['is_important']
            cursor.execute("UPDATE task SET is_important=%s where title=%s  ;", (data,title))
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
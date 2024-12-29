import mysql.connector
from typing import List # for statically typed lists

# Connect to MySQL
connct = mysql.connector.connect(
    host='127.0.0.1',
    passwd='12345',
    user='root',
    auth_plugin='mysql_native_password'
)
cursor = connct.cursor(buffered=True)
user_id = '12345'

cursor.execute("USE to_do")
def create_list(name: str) -> None:
    cursor.execute("INSERT INTO list (name, is_pinned) VALUES (%s, false)", name)
    connct.commit()  

def update_list(list_name: str, **kwargs):
    if 'task_ids' in kwargs:
        cursor.execute("UPDATE lists SET task_ids=%s WHERE title=%s;", (kwargs['task_ids'], list_name))

    if 'title' in kwargs:
        cursor.execute("UPDATE lists SET title=%s WHERE title=%s;", (kwargs['title'], list_name))    
    if 'pinned' in kwargs:
        cursor.execute("UPDATE lists SET is_pinned=%s WHERE title=%s;", (kwargs['pinned'], list_name))
         
    connct.commit()

def add_task(list_name: str, **kwargs) -> None:
    
    cursor.execute("INSERT INTO tasks () VALUES ()")    
    cursor.execute("SELECT * FROM tasks ORDER BY task_id DESC LIMIT 1")
    task_id = cursor.fetchone()[0]
    update_task(task_id, **kwargs)
    
    cursor.execute("SELECT * FROM lists WHERE title=%s", (list_name,))
    current_tasks: str = cursor.fetchone()[0]
    if current_tasks:
        current_tasks += ',' + str(task_id)
    else:
        current_tasks = str(task_id)
    update_list(list_name, task_ids=current_tasks)

    connct.commit()
    
def update_task(task_id: str,**kwargs) -> None:
    cursor.execute("SET SQL_SAFE_UPDATES = 0;")

    if 'title' in kwargs:
        cursor.execute("UPDATE tasks SET title=%s WHERE task_id=%s;", (kwargs['title'], task_id))
        connct.commit()
        
    if 'description' in kwargs:
            data=kwargs['description']
            cursor.execute("UPDATE tasks SET description=%s where task_id=%s  ;", (data,task_id))
            connct.commit()
        
    if 'deadline' in kwargs:
            data=kwargs['deadline']
            cursor.execute("UPDATE tasks SET deadline=%s where task_id=%s  ;", (data,task_id))
            connct.commit()

    if 'pinned' in kwargs:
            data=kwargs['pinned']
            cursor.execute("UPDATE tasks SET is_pinned=%s where task_id=%s;", (data,task_id))
            connct.commit()

    if 'priority' in kwargs:
            data=kwargs['priority']
            cursor.execute("UPDATE tasks SET priority=%s where task_id=%s;", (data,task_id))
            connct.commit()

    if 'checked' in kwargs:
            data=kwargs['checked']
            print('update33', data)
            cursor.execute("UPDATE tasks SET is_checked=%s where task_id=%s  ;", (data,task_id))
            connct.commit()

def delete_task(task_id) -> None:
    cursor.execute("DELETE FROM tasks WHERE task_id=%s;",(task_id,))
    print("done deleting task ")
    connct.commit()

def get_task(task_id) -> List[tuple]:
    cursor.execute("select * from tasks where task_id=%s",(task_id,))
    #task_id title description deadline priority pinned checked
    data = cursor.fetchone()            
    connct.commit()
    return data

def get_user_lists() -> List[tuple]:
    cursor.execute("select * from lists where user_id= %s",(user_id,))
    result=cursor.fetchall()
    connct.commit()

    return result

def add_list(title: str):
    cursor.execute("Insert Into lists (title, is_pinned, user_id) VALUES (%s, false, %s)", (title, user_id))
    connct.commit()

def delete_list(title: str):
    cursor.execute("DELETE FROM lists WHERE title=%s AND user_id=%s", (title, user_id) )
    connct.commit()

def add_email(email,password):
    if email_exist(email): return False

    cursor.execute("insert into accounts (email,pass) values (%s,%s)",(email,password))
    connct.commit()
    return True

def add_google_id(google_id,email):
    if email_exist(email): return False
    
    cursor.execute("insert into accounts (google_id,email) values (%s,%s)",(google_id,email))
    connct.commit()
    return True

def email_exist(email):
    cursor.execute("SELECT * FROM accounts WHERE email=%s", (email,))
    if cursor.fetchone(): return True
    else: return False

def login_email(email, password):    
    cursor.execute("SELECT * FROM accounts WHERE email=%s AND pass=%s", (email, password))
    result = cursor.fetchone() 
    if result: return result[3]

    connct.commit()
    return False 

def login_google(id):
    cursor.execute("SELECT * FROM accounts WHERE google_id=%s", (id,))
    result = cursor.fetchone()
    
    if result: return result[3]

    connct.commit()
    return False


# add_email("elgndi2005@gmail.com", "12345")

# print(login_email("elgndi2005@gmail.com", "12345"))

# from googleauth import authenticate
# data = authenticate()
# print(login_google(data[0]))
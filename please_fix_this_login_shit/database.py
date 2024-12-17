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

def add_email(email,password):
    cursor.execute("insert into google (email,pass) values (%s,%s)",(email,password))
    connct.commit()
    print("done")
def add_google_id(google_id,email):
    cursor.execute("insert into google (google_id,email) values (%s,%s)",(google_id,email))
    connct.commit()
    print("done")
    
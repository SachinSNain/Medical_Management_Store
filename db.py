
#### DB CREDS STORAGE in form of dictionary so that it can be shared and used accross the code easily 

#local code execution DB
DB_CREDS = {
    "host" : "localhost" ,
    "port" : 3306,
    "user": "inventory",
    "password": "passkey123",
    "database" : "inventory"
}

DB_CREDS = {
    "host" : "localhost" ,
    "port" : 3306,
    "user": "pharmacy_db",
    "password": "3$T!FLMurS!RUh5",
    "database" : "pharmacy_db"
}

from functools import wraps

# @wrap

# The @wrap decorator copies the docstring, argument names, and other attributes of the wrapped function to the wrapper function. This is useful for keeping the wrapper function looking like the original function when it is inspected.

# Decorator for providing the cursor and closing the connection after operation

# The decorator I provided is a simple decorator that provides the cursor to the wrapped function and closes the connection after the function has finished executing. This can help to prevent memory leaks and other errors.


import mysql.connector as mysql 



def get_mysql_connection():
  """_summary_

  Returns:
      _type_: _the function returns <Mysql connector object that can be futher used to get the database cursor>_
  """
  mydb = mysql.connect(
  host=DB_CREDS["host"],
  port=DB_CREDS["port"],
  user=DB_CREDS["user"],
  password=DB_CREDS["password"],
  database=DB_CREDS["database"])
  
  return mydb

def with_cursor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = get_mysql_connection()
        cur = conn.cursor()

        try:
            result = func(conn,cur, *args, **kwargs)
        finally:
            cur.close()
            conn.close()

        return result
    return wrapper
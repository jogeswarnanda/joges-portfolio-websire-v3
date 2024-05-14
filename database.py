from sqlalchemy import create_engine, text,Table
import os
from sqlalchemy.sql.selectable import Values
from sqlalchemy.orm import scoped_session, sessionmaker
import psycopg2

db_conn_string = os.environ['DB_CONNECTION_STRING']
from sqlalchemy import create_engine
engine=create_engine(db_conn_string)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
  
def validate_username(user_name,data,insert_status,pwd):
    print("username entered by user:", user_name)
    pwd= " "
    with engine.connect() as conn:
      result = conn.execute(text("SELECT * FROM users where user_name = :username"),
             {"username" : user_name});
      rows = result.all()
      print("rows_new::", rows)
      if len(rows) == 0:
        add_user_to_db(user_name,data)
        insert_status = 'Y'
        return insert_status,pwd
      else:
        print("danger:")
        insert_status = 'N'
        return insert_status,pwd

def verify_login (user_name,data,found_stat,pwd):
  print("username entered by user:", user_name)
  pwd= " "
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM users where user_name = :username"),
           {"username" : user_name});
    rows = result.all()
    print(type(rows))
    print("rows_new@@::", rows)
    #print(rows[0][4])
    if len(rows) == 0:
      found_stat = "N"
      print("set found sta N:")
      return found_stat,pwd
    else:
      print("set found stat Y")
      found_stat = "Y"
      pwd=rows[0][4]
      return found_stat,pwd
      
def add_user_to_db(user_name,data):
  with engine.connect() as conn:
    result1 = conn.execute(text("INSERT INTO users (user_name,user_full_name,user_email,user_password) VALUES(:u_name,:full_name,:email,:password)"),
{"u_name": data.get("username"), "full_name" : data.get("full_name"),"email" : data.get("email"),"password" : data.get("password")});
    conn.commit()


import psycopg2

#returns a cursor
#rember to end your connections when done
def createConnection():
    db_connection = psycopg2.connect(
    database="428Project_Team-Enforcers",
    user="postgres",
    password="Code1Lock1",
    host="localhost",
    port="5432"
   )
    
    return db_connection
#if the DB is empty adds two testers and a John Doe
#all of there passwords are set to 123 
#one of them is an author no idea which
def fillDB():
    db_connection = createConnection() 
    cursor = db_connection.cursor()
    USERNAME = ("Tester1","Tester2","John Doe")
    sql = """"
        INSERT INTO ACCOUNT (User) 
        PASSWORD("123")
        USER_ID(%s)

    """
    for  User in USERNAME:
        cursor.execute(sql, (User,"123",))
    
    User_id = cursor.fetchone()[0]
    sql = """
        INSERT INTO AUTHOR(User_id) ID(%s) 
    """
    cursor.execute(sql, (User_id,))
    cursor.close()
    db_connection.commit()
    db_connection.close()

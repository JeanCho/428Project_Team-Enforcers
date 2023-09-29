
#returns a cursor 
import psycopg2


def createConnection():
    db_connection = psycopg2.connect(
    database="428Project_Team-Enforcers",
    user="postgres",
    password="Code1Lock1",
    host="localhost",
    port="5432"
   )
    
    return db_connection
    
def ifEmpty():
    db_connection = createConnection() 
    cursor = db_connection.cursor()
    USERNAME = ("Tester1","Tester2","John Doe")
    sql = """"
        INSERT INTO Account (User) 
        PASSWORD("123")
        USER_ID(%s)

    """
    for  User in USERNAME:
        cursor.execute(sql, (User,"123",))
    
    User_id = cursor.fetchone()[0]
    sql = """
        INSERT INTO Author 
    """
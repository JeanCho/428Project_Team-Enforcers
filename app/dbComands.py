

import psycopg2

#returns a cursor
#rember to end your connections when done
def createConnection():
    db_connection = psycopg2.connect(
    database="428Project_Team-Enforcers",
    user="postgres",
    password="Code1Lock1",#durian123
    host="localhost",
    port="5432"
   )
    
    return db_connection
#if the DB is empty adds two testers and a John Doe
#all of there passwords are set to 123 
#one of them is an author no idea which
# def fillDB():
#     print("\nFilling DB with testers\n")
#     db_connection = createConnection() 
#     cursor = db_connection.cursor()
#     USERNAME = ("Tester1","Tester2","John Doe")
#     sql = """
#         INSERT INTO ACCOUNT(USERNAME, PASSWORD, USER_ID) 
#         VALUES(%s, %s,%s)

#     """
#     x = 1
#     Pass = "123"
#     for  Name in USERNAME:
#         cursor.execute(sql, (Name,Pass,x ))
#         x = x +1
    
#     User_id = 3
#     sql = """
#         INSERT INTO AUTHOR(USER_ID, ID) VALUES(%s,%s) 
#     """
#     cursor.execute(sql, (User_id, 1))

#     sql = """
#         INSERT INTO ARTICLE(ID, AUTHOR_ID, TITLE, ARTICLE)
#         VALUES(%s, %s, %s, %s)
#         """
    
#     cursor.execute(sql,(1,1,"HELLO WORLD","This is a test of hello world"))
#     cursor.execute(sql,(2,1,"Strange_Test","this is a writing test created for testing purposes"))
#     cursor.close()
#     db_connection.commit()
#     db_connection.close()

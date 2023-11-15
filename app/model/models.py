import psycopg2;
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT;
from dbComands import createConnection

def createTable():
   db_connection = createConnection()
   
   cursor = db_connection.cursor()

   ##sql = [] changing to this to clean up the exucutes later but for testing doing it 1 at a time
   
   # im sure password has some special rules but I don't know them yet
   # ill change it later.
   # thinking about leaving password as is for an easy change later
   sql = """
      CREATE TABLE ACCOUNT(
         USER_ID SERIAL PRIMARY KEY,
         USERNAME VARCHAR(20) UNIQUE,
         PASSWORD VARCHAR(20) 
      )
      """

   cursor.execute(sql)

   
   # implement relational database for a few of these
   # relation with the user who can act as an AUTHOR
   sql = '''CREATE TABLE AUTHOR (
      ID SERIAL PRIMARY KEY,
      USER_ID INT,
      CONSTRAINT fk_account FOREIGN KEY(USER_ID) REFERENCES ACCOUNT(USER_ID)
      );'''

   cursor.execute(sql)

   
   #Relation with who posted it
   sql = '''CREATE TABLE ARTICLE (
      ID SERIAL PRIMARY KEY,
      AUTHOR_ID INT,
      TITLE TEXT NOT NULL,
      ARTICLE TEXT NOT NULL,
      CONSTRAINT fk_author FOREIGN KEY(AUTHOR_ID) REFERENCES AUTHOR(ID) 
      );'''

   cursor.execute(sql)

   
   #Relation with who posted it and where it was posted
   sql = '''CREATE TABLE COMMENT (
      USER_ID INT,
      COMMIT VARCHAR(500),
      ARTICLE_ID INT,
      CONSTRAINT fk_user FOREIGN KEY(USER_ID) REFERENCES ACCOUNT(USER_ID),
      CONSTRAINT fk_article FOREIGN KEY(ARTICLE_ID) REFERENCES ARTICLE(ID)
      );'''

   cursor.execute(sql)
   cursor.close()
   db_connection.commit()
   db_connection.close()

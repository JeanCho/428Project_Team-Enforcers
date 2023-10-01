import psycopg2;
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT;


def createTable():
   db_connection = psycopg2.connect(
    database="428Project_Team-Enforcers",
    user="postgres",
    password="durian123",
    host="localhost",
    port="5432"
   )
   
   cursor = db_connection.cursor()

   ##sql = [] changing to this to clean up the exucutes later but for testing doing it 1 at a time
   
   # im sure password has some special rules but I don't know them yet
   # ill change it later.
   # thinking about leaving password as is for an easy change later
   sql = """
      CREATE TABLE ACCOUNT(
         USER_ID INT PRIMARY KEY,
         USERNAME VARCHAR(20) NOT NULL,
         PASSWORD VARCHAR(20) 
      )
      """

   cursor.execute(sql)

   
   # implement relational database for a few of these
   # relation with the user who can act as an AUTHOR
   sql = '''CREATE TABLE AUTHOR (
      ID INT PRIMARY KEY,
      USER_ID INT,
      CONSTRAINT fk_account FOREIGN KEY(USER_ID) REFERENCES ACCOUNT(USER_ID)
      );'''

   cursor.execute(sql)

   
   #Relation with who posted it
   sql = '''CREATE TABLE ARTICLE (
      ID INT PRIMARY KEY,
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

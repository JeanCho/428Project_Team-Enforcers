import psycopg2;
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT;
from app import db_connection;

cursor = db_connection.cursor()

##sql = [] changing to this to clean up the exucutes later but for testing doing it 1 at a time
cursor.execite("DROP TABLE IF EXISTS USER")
# im sure password has some special rules but I don't know them yet
# ill change it later.
#
sql = '''CREATE TABLE USER(
   USER_ID INT,
   USERNAME CHAR(20) NOT NULL,
   PASSWORD CHAR(20)
)'''

cursor.execite(sql)

cursor.execite("DROP TABLE IF EXISTS AUTHOR")
# implement relational database for a few of these
# relation with the user who can act as an AUTHOR
sql = '''CREATE TABLE AUTHOR(
   USER_ID INT, 
   ARTICLE_ID INT
)'''

cursor.execite(sql)

cursor.execite("DROP TABLE IF EXISTS ARTICLE")
#Relation with who posted it
sql = '''CREATE TABLE ARTICLE(
   ARTICLE_ID INT,
   USER_ID INT,
   ARTICLE CHAR(2500) 
)'''

cursor.execite(sql)

cursor.execite("DROP TABLE IF EXISTS COMMIT")
#Relation with who posted it and where it was posted
sql = '''CREATE TABLE COMMIT(
   USER_ID INT,
   COMMIT CHAR(500),
   ARTICLE_ID INT 
)'''

cursor.execite(sql)
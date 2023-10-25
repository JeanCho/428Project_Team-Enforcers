
import psycopg2
from dbComands import createConnection


def get_articals():
    db_connection = createConnection()
    cursor = db_connection.cursor()
    sql = """ 
        select * from ARTICLE
        """
    print("selecting all articles in DB")
    cursor.execute(sql)
    articalRecords = cursor.fetchall 
    cursor.close()
    db_connection.close()
    return articalRecords

def get_artical_from_title(title):
    db_connection = createConnection()
    curr = db_connection.cursor()
    sql = """
        select * from ARTICLE where title = 
    """
    sql = sql +  " '" + title + "' "
    print(sql)
    curr.execute(sql)
    artical = curr.fetchall()
    curr.close()
    db_connection.close()
    return artical

def get_author_from_id(id):
    db_connection = createConnection()
    curr = db_connection.cursor()
    sql = """
        select * from AUTHOR where '
    """

    sql = sql + str(id) + "' "

    curr.execute(sql)
    author = curr.fetchall()
     
    authorId = author[0][1]
    print("making it clear what is being printed " + str(authorId))
    sql2 = """
        select * from ACCOUNT where USER_ID ='
    """ + str(authorId) + "' "


    curr.execute(sql2)
    username= curr.fetchall()
    return username[0][1]

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
        select * from article
        where title = %s 
    """
    curr.execute(sql(title))
    artical = curr.fetchall()
    return artical

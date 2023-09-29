
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

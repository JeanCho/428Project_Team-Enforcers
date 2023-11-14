
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
        select * from ACCOUNT where USER_ID =' """ + str(authorId) + "' "


    curr.execute(sql2)
    username= curr.fetchall()
    return username[0][1]

def get_comments_from_article_id(id):
    db_connection = createConnection()
    curr = db_connection.cursor()
    sql = " select commit from COMMENT where ARTICLE_ID = '"+ str(id)+"' "
    curr.execute(sql)
    comments = curr.fetchall()
    print(comments)
    curr.close()
    db_connection.close()
    return comments

def get_user_id(username):
    db_connection = createConnection()
    curr = db_connection.cursor()
    print(username)
    sql = "select user_id from ACCOUNT where username = '"+ str(username) +"' "
    
    print(sql)
    curr.execute(sql)
    id = curr.fetchall()
    curr.close()
    db_connection.close()
    print("Account id of"+ str(id))
    return id

def add_comment(comment, artId, user_id):
    db_connection = createConnection()
    curr = db_connection.cursor()
    sql = """
        INSERT INTO COMMENT(USER_ID, COMMIT, ARTICLE_ID) 
        VALUES(%s, %s,%s)

    """
    
    curr.execute(sql,(user_id,comment,artId)
                 )
    curr.close()
    db_connection.commit()
    db_connection.close()
    return
    





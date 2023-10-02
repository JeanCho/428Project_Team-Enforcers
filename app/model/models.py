import psycopg2;
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT;
from dbComands import createConnection

def createTable():
    db_connection = createConnection()
    cursor = db_connection.cursor()

    try:
        # Create ACCOUNT table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS public.ACCOUNT (
                USER_ID SERIAL PRIMARY KEY,
                USERNAME VARCHAR(255) NOT NULL,
                PASSWORD VARCHAR(255)
            );
        """)

        # Create AUTHOR table with a foreign key reference to ACCOUNT
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS public.AUTHOR (
                ID SERIAL PRIMARY KEY,
                USER_ID INT,
                CONSTRAINT fk_account FOREIGN KEY (USER_ID) REFERENCES public.ACCOUNT (USER_ID)
            );
        """)

        # Create ARTICLE table with a foreign key reference to AUTHOR
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS public.ARTICLE (
                ID SERIAL PRIMARY KEY,
                AUTHOR_ID INT,
                TITLE TEXT NOT NULL,
                ARTICLE TEXT NOT NULL,
                CONSTRAINT fk_author FOREIGN KEY (AUTHOR_ID) REFERENCES public.AUTHOR (ID)
            );
        """)

        # Create COMMENT table with foreign key references to ACCOUNT and ARTICLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS public.COMMENT (
                USER_ID INT,
                COMMIT VARCHAR(500),
                ARTICLE_ID INT,
                CONSTRAINT fk_user FOREIGN KEY (USER_ID) REFERENCES public.ACCOUNT (USER_ID),
                CONSTRAINT fk_article FOREIGN KEY (ARTICLE_ID) REFERENCES public.ARTICLE (ID)
            );
        """)

        db_connection.commit()
    except Exception as e:
        db_connection.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        db_connection.close()

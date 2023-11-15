from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from flask_login import current_user, LoginManager
import psycopg2
from model.models import createTable
<<<<<<< HEAD
from dbComands import createConnection, fillDB
from Controller.forms import get_articals, get_artical_from_title, get_author_from_id, get_comments_from_article_id
from Controller.forms import get_user_id, get_comments_from_article_id, add_comment                
=======
from dbComands import createConnection
from Controller.forms import get_articals, get_artical_from_title, get_author_from_id
>>>>>>> controller_setup

app = Flask(__name__)

# Configure your PostgreSQL connection
db_connection = createConnection()

##createTable()

cursor = db_connection.cursor()

# count = [] 
# cursor.execute("SELECT count(*) from ACCOUNT", count)
# result = cursor.fetchone()
# print(result)
# if(result[0] == 0):
#     fillDB()


app.secret_key = 'your_secret_key'


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET','POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM ACCOUNT WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone() 
    cursor.close()
    
    if user:
        session['username'] = username
        flash('Logged in successfully')
        return redirect(url_for('dashboard'))
    else:
        return "Login failed. Please try again."
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        cursor = db_connection.cursor()
        cursor.execute("SELECT username FROM ACCOUNT WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user:
            print('The username exists! Try a new one')
            return render_template('register.html')
        else:
            print("Successfully registered!")
            sql = """ INSERT INTO ACCOUNT(USERNAME, PASSWORD) VALUES(%s, %s)"""
            cursor.execute(sql, (username, password))
            cursor.execute("SELECT user_id FROM ACCOUNT ORDER BY user_id DESC LIMIT 1")
            user = cursor.fetchone()
            print(user)
            sql1 = """ INSERT INTO AUTHOR(USER_ID) VALUES(%s) """
            cursor.execute(sql1, (user))
            db_connection.commit()
            cursor.close()
            return redirect(url_for('dashboard'))
    else:
        return render_template('register.html')
            
        

   

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' in session:
        
        db_connection = createConnection()
        curr = db_connection.cursor()
        curr.execute('SELECT TITLE FROM ARTICLE')
        articles = curr.fetchall()
        art =[]
        for a in articles:
            art.append(a[0])
        curr.close()
        db_connection.close()
        return render_template('dashboard.html', art = art)
    else:
        return redirect(url_for('home'))

@app.route('/view_article/<title>')
def view_article(title):
    #print(title[0][0])
    
    article = get_artical_from_title(title)
    # Check if the article exists
    username = get_author_from_id(article[0][1])
    #pulls all comments made about this article
    comments = get_comments_from_article_id(article[0][0])
    comment =[]
    for comm in comments:
        comment.append(comm[0])
    print(article)
    if article is None:
        # Handle the case where the article doesn't exist (e.g., display an error message)
        return render_template('error.html', message='Article not found')

    story = {
        'author_id': username,
        'title':  article[0][2],
        'content':  article [0][3],
        'artId': article [0][0]
    }   
    return render_template('story.html', story=story, comments = comment)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/create_article', methods = ['GET','POST'])
def create_article():
    if 'username' in session: 
        if request.method == 'POST':
            new_title = request.form.get('title')
            new_content = request.form.get('content')
            cursor = db_connection.cursor()
            cursor.execute("select user_id from ACCOUNT where username = '" + str(session.get('username')) + "'")
            user_id = cursor.fetchall() 
            sql = """ INSERT INTO ARTICLE(AUTHOR_ID, TITLE, ARTICLE) VALUES(%s, %s, %s)"""
            cursor.execute(sql, (user_id[0], new_title,new_content))
            db_connection.commit()
            return redirect(url_for('dashboard'))
        else:
            return render_template('createarticle.html') 
    else:
        return render_template('createarticle.html') 

@app.route('/postComment/<storyId>/<title>',methods=['POST'])
def postComment(storyId, title):
    comment = request.form['COMMIT']
    #story = request.form['story']
    print(storyId)
    print(title)
    if 'username' in session:

        user_id = get_user_id(session.get('username'))
        add_comment(comment, storyId, user_id[0][0])
        return redirect(url_for('view_article', title = title))
    
    return redirect(url_for('story.html'))

if __name__ == '__main__':
    app.run(debug=True)
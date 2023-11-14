from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from model.models import createTable
from dbComands import createConnection, fillDB
from Controller.forms import get_articals, get_artical_from_title, get_author_from_id, get_comments_from_article_id
from Controller.forms import get_user_id, get_comments_from_article_id, add_comment                

app = Flask(__name__)

# Configure your PostgreSQL connection
db_connection = createConnection()

##createTable()

cursor = db_connection.cursor()

count = [] 
cursor.execute("SELECT count(*) from ACCOUNT", count)
result = cursor.fetchone()
print(result)
if(result[0] == 0):
    fillDB()


app.secret_key = 'your_secret_key'


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM ACCOUNT WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    
    if user:
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return "Login failed. Please try again."

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

@app.route('/create')
def create():
    if 'username' in session:
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
import time
from flask import Flask, render_template, request, redirect, url_for, session, flash, g

#from flask_login import current_user, LoginManager
import psycopg2
from model.models import createTable

from dbComands import createConnection
from Controller.forms import get_articals, get_artical_from_title, get_author_from_id, get_comments_from_article_id
from Controller.forms import get_user_id, get_comments_from_article_id, add_comment                
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import boto3
from botocore.exceptions import NoCredentialsError


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to send logs to AWS CloudWatch Logs
def send_logs(log_group, log_stream, log_data):
    try:
        # Configure your AWS credentials and region
        aws_access_key_id = 'AKIAUFQ46Q3NUHBBGKXY'
        aws_secret_access_key = 'OH2lfw2xUqm4zhHNxydIFFwwGRSg7Rz2cmKJZnmz'
        aws_region = 'us-west-2'

        client = boto3.client('logs', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

        # Create or retrieve the log group and log stream
        try:
            client.create_log_group(logGroupName=log_group)
            print(f"Log group '{log_group}' created successfully.")
        except client.exceptions.ResourceAlreadyExistsException:
            print(f"Log group '{log_group}' already exists.")
        print("Sending loggss...")
        response = client.create_log_stream(logGroupName=log_group, logStreamName=log_stream)

        # Send logs to CloudWatch Logs
        response = client.put_log_events(
            logGroupName=log_group,
            logStreamName=log_stream,
            logEvents=[
                {
                    'timestamp': int(round(time.time() * 1000)),
                    'message': log_data,
                },
            ],
        )

        print(f"Logs sent successfully to {log_group}/{log_stream}")
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(f"Error: {e}")
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
) #Using python limiter to prevent ddos
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

# Add a function for request validation
def validate_request():
    # Validate that the request has a valid User-Agent header
    user_agent = request.headers.get('User-Agent')
    if not user_agent or 'Mozilla' not in user_agent:
        return False
    # invalidate that the request has suspicous headers
    suspicious_headers = ['Proxy-Connection', 'X-Forwarded-For']
    for header in suspicious_headers:
        if request.headers.get(header):
            return False
    
    return True


@app.route('/')
@limiter.limit("5 per minute")
def home():

    if not validate_request():
        print("Request Validation Failed!")
        logger.info('reqeust validation fail')
        send_logs("428app", "request", 'reqeust validation fail')
        return render_template('error.html', message='Invalid request')
    logger.info('Home page visited')
    send_logs("428app", "home page", 'Home page visited')
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Adjust the rate limit as needed
def login():

    if not validate_request():
        logger.info('reqeust validation fail')
        send_logs("428app", "request", 'reqeust validation fail')
        return render_template('error.html', message='Invalid request')
    username = request.form['username']
    password = request.form['password']
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM ACCOUNT WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone() 
    cursor.close()
    
    if user:
        session['username'] = username
        flash('Logged in successfully')
        logger.info('login')
        send_logs("428app", "login", 'Logged in successfully')
        return redirect(url_for('dashboard'))
    else:
        logger.info('login fail')
        send_logs("428app", "login", 'Login fail')
        return "Login failed. Please try again."
    
@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Adjust the rate limit as needed
def register():
    if not validate_request():
        logger.info('reqeust validation fail')
        send_logs("428app", "request", 'reqeust validation fail')
        return render_template('error.html', message='Invalid request')
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        cursor = db_connection.cursor()
        cursor.execute("SELECT username FROM ACCOUNT WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user:
            print('The username exists! Try a new one')
            logger.info('register')
            send_logs("428app", "register", 'register fail')
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
            logger.info('register')
            send_logs("428app", "register", 'register success')
            return redirect(url_for('dashboard'))
    else:
        return render_template('register.html')
            
        

   

@app.route('/dashboard', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Adjust the rate limit as needed
def dashboard():
    if not validate_request():
        logger.info('reqeust validation fail')
        send_logs("428app", "request", 'reqeust validation fail')
        return render_template('error.html', message='Invalid request')
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
        logger.info('get dashboard')
        send_logs("428app", "dashboard", 'get dashboard success')
        return render_template('dashboard.html', art = art)
    else:
        logger.info('get dashboard fail rediect to home')
        send_logs("428app", "dashboard", 'get dashboard fail redirect to home')
        return redirect(url_for('home'))

@app.route('/view_article/<title>')
@limiter.limit("5 per minute")  # Adjust the rate limit as needed
def view_article(title):
    if not validate_request():
        logger.info('reqeust validation fail')
        send_logs("428app", "request", 'reqeust validation fail')
        return render_template('error.html', message='Invalid request')
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
        logger.info('view article fail')
        send_logs("428app", "article", 'view article fail no article')
        return render_template('error.html', message='Article not found')

    story = {
        'author_id': username,
        'title':  article[0][2],
        'content':  article [0][3],
        'artId': article [0][0]
    }   
    logger.info('view article')
    send_logs("428app", "article", 'view article success')
    return render_template('story.html', story=story, comments = comment)

@app.route('/logout')
@limiter.limit("5 per minute")  # Adjust the rate limit as needed
def logout():
    session.pop('username', None)
    logger.info('log out')
    send_logs("428app", "log out", 'log out success')
    return redirect(url_for('home'))

@app.route('/create_article', methods = ['GET','POST'])
@limiter.limit("5 per minute")  # Adjust the rate limit as needed
def create_article():
    if not validate_request():
        logger.info('reqeust validation fail')
        send_logs("428app", "request", 'reqeust validation fail')
        return render_template('error.html', message='Invalid request')
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
            logger.info('create article')
            send_logs("428app", "create article", 'create article success')
            return redirect(url_for('dashboard'))
        else:
            logger.info('create article fail')
            send_logs("428app", "create article", 'create article fail')
            return render_template('createarticle.html') 
    else:
        return render_template('createarticle.html') 

@app.route('/postComment/<storyId>/<title>',methods=['POST'])
@limiter.limit("5 per minute")  # Adjust the rate limit as needed
def postComment(storyId, title):
    if not validate_request():
        logger.info('reqeust validation fail')
        send_logs("428app", "request", 'reqeust validation fail')
        return render_template('error.html', message='Invalid request')
    comment = request.form['COMMIT']
    #story = request.form['story']
    print(storyId)
    print(title)
    if 'username' in session:

        user_id = get_user_id(session.get('username'))
        add_comment(comment, storyId, user_id[0][0])
        logger.info('post comment')
        send_logs("428app", "post comment", 'post comment success')
        return redirect(url_for('view_article', title = title))
    logger.info('post comment fail')
    send_logs("428app", "post comment", 'post comment fail')
    return redirect(url_for('story.html'))

if __name__ == '__main__':
    app.run(debug=True)
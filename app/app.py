from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from model.models import createTable
from dbComands import createConnection, fillDB

app = Flask(__name__)

# Sample articles (you can replace this with actual database queries)
sample_articles = []


# Configure your PostgreSQL connection
db_connection = createConnection()

createTable()

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

@app.route('/dashboard')
def dashboard():
    return render_template("Dashboard.html", art=sample_articles)

@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        # Create a dictionary for the new article
        new_article = {
            "id": len(sample_articles) + 1,  # Assign a unique ID
            "title": title,
            "content": content
        }
        
        sample_articles.append(new_article)
        
        # Redirect back to the dashboard
        return redirect(url_for('dashboard'))
    
    return render_template("add_article.html")
def get_article_by_id(article_id):
    # Create a database connection
    db_connection = createConnection()
    
    try:
        cursor = db_connection.cursor()
        
        # Define your SQL query to fetch the article by ID
        sql = "SELECT ID, AUTHOR_ID, TITLE, ARTICLE FROM ARTICLE WHERE ID = %s"
        
        # Execute the query with the article_id as a parameter
        cursor.execute(sql, (article_id,))
        
        # Fetch the article record
        article_record = cursor.fetchone()
        
        # Check if the article exists
        if article_record:
            # Create a dictionary with the article details for easier access in the template
            article = {
                'id': article_record[0],
                'author_id': article_record[1],
                'title': article_record[2],
                'content': article_record[3]
            }
            return article
        else:
            # Return None if the article doesn't exist
            return None
    except Exception as e:
        # Handle any exceptions that may occur during the database operation
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        db_connection.close()
    
@app.route('/view_article/<int:article_id>')
def view_article(article_id):
    # Retrieve the article from the database based on the article_id
    article = get_article_by_id(article_id)

    # Check if the article exists
    if article is None:
        # Handle the case where the article doesn't exist (e.g., display an error message)
        return render_template('error.html', message='Article not found')

    return render_template('article.html', article=article)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
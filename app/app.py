from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from model.models import createTable
from dbComands import createConnection, fillDB

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
        return render_template('dashboard.html')
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/create')
def create():
    if 'username' in session:
        return render_template('createarticle.html')

if __name__ == '__main__':
    app.run(debug=True)
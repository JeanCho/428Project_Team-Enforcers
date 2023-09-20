from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2

app = Flask(__name__)

# Configure your PostgreSQL connection
db_connection = psycopg2.connect(
    database="428Project_Team-Enforcers",
    user="postgres",
    password="mustafa",
    host="localhost",
    port="5432"
)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM user_credentials WHERE username = %s AND password_hash = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    
    if user:
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return "Login failed. Please try again."

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f"Welcome, {session['username']}! This is your dashboard."
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.secret_key = 'your_secret_key'
    app.run(debug=True)

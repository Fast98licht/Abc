from flask import Flask, request, render_template_string, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'somesecretkey'

DATABASE = 'users.db'

def query_db(query, args=(), one=False):
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute(query, args)
        rv = cur.fetchall()
        return (rv[0] if rv else None) if one else rv

def insert_db(query, args=()):
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute(query, args)
        conn.commit()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # For security, you should hash this password before storing.
        
        # Check if username exists
        user = query_db('SELECT * FROM users WHERE username=?', [username], one=True)
        if user:
            flash('Username already exists.')
            return redirect(url_for('register'))
        
        insert_db('INSERT INTO users (username, password) VALUES (?, ?)', [username, password])
        flash('Registered successfully.')
        return redirect(url_for('login'))
    return render_template_string(open("registration.html").read())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # In practice, you'd hash the password and check against the hashed value.
        
        user = query_db('SELECT * FROM users WHERE username=? AND password=?', [username, password], one=True)
        if user:
            flash('Login successful.')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.')
            return redirect(url_for('login'))
    return render_template_string(open("login.html").read())

@app.route('/dashboard')
def dashboard():
    return 'Welcome to the dashboard!'

if __name__ == '__main__':
    app.run(debug=True)

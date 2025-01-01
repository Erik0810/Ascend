from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from __init__ import DATABASE

bp = Blueprint('loginSys', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

#REMOVE LATER
MOCK_USERS = {
    "test": "admin"
}

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        #Get correct pw
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT password, id FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        #Validate credentials
        print(result)
        if result and result[0] == password:
            session['user'] = username
            userID = result[1]
            session['user_id'] = userID
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash("Invalid username or password", "danger")
    
    return render_template('login.html')

@bp.route('/register')
def register():
    return render_template("register.html")

@bp.route('/registerSuccess', methods=['POST'])
def registerSuccess():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', 
                   (username, email, password))
    conn.commit()
    conn.close()
    return render_template("registerSuccess.html")
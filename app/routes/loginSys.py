from flask import Blueprint, render_template, request, redirect, send_from_directory, url_for, flash, session
import sqlite3
from __init__ import DATABASE
import bcrypt

bp = Blueprint('loginSys', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

#REMOVE LATER
MOCK_USERS = {
    "test": "admin"
}

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        input_password = request.form.get('password')

        #Get correct pw
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT password, id FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        
        #Validate credentials
        if result is None:
            flash("Invalid username or password", "danger")
            return render_template('login.html')
        if bcrypt.checkpw(input_password.encode('utf-8'), result[0]):
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

    # Hash pw
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        flash('Username already taken. Please choose another one.', 'danger')
        return redirect(url_for('loginSys.register'))
    
    cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', 
                   (username, email, hashed_password))
    conn.commit()
    conn.close()
    return render_template("registerSuccess.html")
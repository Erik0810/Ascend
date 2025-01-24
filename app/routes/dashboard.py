from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from __init__ import DATABASE
from datetime import datetime

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')
def dashboard():
    from run import app
    #Remove later!!!!!!!!!!!!!!!!!!!!!!!
    if app.config['DEBUG'] and 'user' not in session:
        session['user'] = "OscarWilde"
        session["user_id"] = 1
    #Not this
    if 'user' not in session:
        return redirect(url_for('loginSys.home'))
    username = session['user']
    userID =get_user_id()

    #Database for displaying climbs
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT route_name, grade, location, climb_date FROM climbs WHERE user_id = ?
    ''', (userID,))
    climbs = cursor.fetchall()
    conn.close()

    return render_template("dashboard.html",username=username, climbs=climbs)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('loginSys.login'))

@bp.route('/profile')
def profile():
    return render_template("profile.html", username=session["user"])

@bp.route('/submit_climb', methods=['POST'])
def submit_climb():
    user_id = get_user_id()

    route_name = request.form['route_name']
    grade = request.form['grade']
    location = request.form['location']

    #Insert to database
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO climbs (route_name, grade, location, user_id) 
            VALUES (?, ?, ?, ?)
        ''', (route_name, grade, location, user_id))
        conn.commit()

    return redirect(url_for('dashboard.dashboard'))

@bp.route('/get_data')
def get_data():
    #Database for chart
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT grade, climb_date FROM climbs WHERE user_id = ? ORDER BY climb_date
    ''', (get_user_id(),))
    chart_data = cursor.fetchall()
    conn.close()
    grades=[]
    dates=[]
    for climb in chart_data:
        grade, date = climb
        grades.append(grade)
        dates.append(date)
    return {'grades': grades, 'dates': dates}

def get_user_id():
    
    user_id = session.get('user_id')  

    #Redirect to login if issue is encountered
    if not user_id:
        flash("User not found or session expired.", "error")
        return redirect(url_for('loginSys.home'))  

    return int(user_id)


from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from __init__ import DATABASE
from datetime import datetime
from utils import get_user_id

bp = Blueprint('profile', __name__)

@bp.route('/profile')
def profile():
    userID = get_user_id()
    
    #Database query for fetching user information
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT email, creation_date FROM users WHERE id = ?
    ''', (userID,))
    user_info = cursor.fetchall()
    conn.close()

    return render_template("profile.html", username=session["user"], user_info=user_info)

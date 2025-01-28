import os
from flask import Flask
import sqlite3
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.db')
def create_app():
    app = Flask(__name__)

    #Fix pw with environment variable, remove debug mode
    app.config['SECRET_KEY'] = 'midlertidigPassord'
    app.config['DEBUG'] = True

    #Set routes from blueprints
    from routes.loginSys import bp as loginRoutes_bp
    app.register_blueprint(loginRoutes_bp)
    from routes.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    #Database init, add separate tables for climbs etc
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            creation_date TEXT NOT NULL DEFAULT CURRENT_DATE
        )
    """)
    #Climbs table with user_id as a foreign key
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS climbs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            route_name TEXT NOT NULL,
            grade TEXT NOT NULL,
            location TEXT NOT NULL,
            climb_date TEXT NOT NULL DEFAULT CURRENT_DATE,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()
    return app
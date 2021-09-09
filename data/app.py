
from flask import g, Flask, app, render_template, redirect
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'music_dashboard.db'

def get_db():
    db = getattr(g, '_music_dashboard', None) 
    if db is None:
        db= g._music_dahboard = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row       
    return db

def query_db(query, args=(), one=False):
    with app.app_context():
        cur = get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
    return (rv[0] if rv else None) if one else rv

  

@app.teardown_appcontext
def close_connection (exception):
    db = getattr(g, 'music_dashbaord', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    data = query_db('select * from albums')
    return render_template('index.html', data = data)


if __name__ == "__main__":
    app.run(debug=True)
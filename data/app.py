
from flask import g, Flask, app, render_template, redirect
import sqlite3
import os
# assign instance of Flask
app = Flask(__name__)
# db path
DATABASE = 'music_dashboard.db'
# create db connection and create a row factory
def get_db():
    db = getattr(g, '_music_dashboard', None) 
    if db is None:
        db= g._music_dahboard = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row       
    return db
# set query with in a flask context for db
def query_db(query, args=(), one=False):
    with app.app_context():
        cur = get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
    return (rv[0] if rv else None) if one else rv

  
# create teardown for db connection
@app.teardown_appcontext
def close_connection (exception):
    db = getattr(g, 'music_dashbaord', None)
    if db is not None:
        db.close()
# create index route
@app.route('/')
def index():
    data = query_db('select * from albums')
    return render_template('index.html', data = data)

# run app in debug mode for developement 
if __name__ == "__main__":
    app.run(debug=True)
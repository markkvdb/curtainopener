from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from .functions import *
from .curtain import *

import os
import sqlite3

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'curtainopener.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('CURTAIN_OPENER_SETTINGS', silent=True)

###################

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def get_curtain():
    """Creates variable indicating status curtain."""
    if not hasattr(g, 'curtain'):
        g.curtain = Curtain(False)
    return g.curtain

def init_status_curtain(status):
    curtain_status = get_curtain()
    curtain_status.opened = status

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route('/')
def dashboard():
    db = get_db()
    curtain = get_curtain()
    cur = db.execute('select * from entries WHERE date >= ' + date_selector(0,0) + '')
    entries = cur.fetchall()
    return render_template('dashboard.html', entries=entries, status=curtain.opened)

@app.route('/add', methods=['POST'])
def add_entry():
    hours = request.form['hours']
    minutes = request.form['minutes']
    if not valid_time(int(hours), int(minutes)):
        flash('Invalid time.')
        curtain = get_curtain()
        curtain.opened = True
        return redirect(url_for('dashboard'))

    db = get_db()
    properdate = date_selector(int(hours), int(minutes))
    print(properdate)
    db.execute('insert into entries (hours, minutes, date) values (?,?,?)', [hours, minutes, properdate])
    db.commit()
    flash('New alarm was set.')
    return redirect(url_for('dashboard'))

@app.route('/delete', methods=['POST'])
def delete_entry():
    db = get_db()
    id = int(request.form['id'])
    db.execute('delete from entries where id=?', (id,))
    db.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run()

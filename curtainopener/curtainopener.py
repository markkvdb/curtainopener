from datetime import datetime

from flask import request, redirect, url_for, render_template, flash

from .functions import *
from .variables import *


@app.route('/')
def dashboard():
    global variableDict
    db = get_db()
    time_now = datetime.now()
    cur = db.execute('select * from entries WHERE date >= ' + time_now.strftime("%Y-%m-%d") + ' AND done = 0 ORDER BY date, hours, minutes')
    entries = cur.fetchall()
    return render_template('dashboard.html', entries=entries, opened=variableDict['curtain_open'])


@app.route('/add', methods=['POST'])
def add_entry():
    hours = request.form['hours']
    minutes = request.form['minutes']
    open = False

    if not valid_time(int(hours), int(minutes)):
        flash('Invalid time.')
        return redirect(url_for('dashboard'))

    if 'open' in request.form:
        open = True

    db = get_db()
    cur = db.cursor().execute('select value from settings WHERE id=1')
    seconds_till_start = cur.fetchone()[0] * 60
    alarm = Alarm(hours, minutes, open, seconds_till_start)
    cursor = db.cursor()
    proper_date = alarm.date_to_str()
    cursor.execute('insert into entries (hours, minutes, date, open) values (?,?,?,?)', [alarm.hours, alarm.minutes,
                                                                                     proper_date, alarm.open])
    db.commit()
    alarm.set_id(cursor.lastrowid)
    curtain_job_controller_add(alarm)
    flash('New alarm was set.')

    return redirect(url_for('dashboard'))


@app.route('/delete', methods=['POST'])
def delete_entry():
    db = get_db()
    cursor = get_db().cursor()
    id = int(request.form['id'])
    cursor.execute('update entries set done = 1 where id=?', (id,))
    db.commit()
    return redirect(url_for('dashboard'))


@app.route('/settings')
def settings():
    db = get_db()
    cursor = db.cursor()
    cur = cursor.execute('select value from settings WHERE id=1')
    value = cur.fetchone()[0]
    return render_template('settings.html', time_value=value)


@app.route('/change_settings', methods=['POST'])
def change_settings():
    time_value = int(request.form['time_before_start'])
    db = get_db()
    cursor = db.cursor()
    cursor.execute('update settings set value = ? where id=1', (time_value,))
    db.commit()
    return redirect(url_for('settings'))

@app.before_first_request
def start_job_thread():
    t = threading.Thread(target=job_worker, daemon=True)
    t.start()


if __name__ == '__main__':
    app.run(use_reloader=False)

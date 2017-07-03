from datetime import datetime

from flask import request, redirect, url_for, render_template, flash

from .functions import *
from .variables import *


@app.route('/')
def dashboard():
    global variableDict
    db = get_db()
    time_now = datetime.now()
    cur = db.execute('select * from entries WHERE date >= ' + time_now.strftime("%Y-%m-%d")
                     + ' AND done = 0 ORDER BY date, hours, minutes')
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
    cur = db.cursor().execute('select value from settings')
    entries = cur.fetchall()
    seconds_till_start = entries[0][0] * 60
    speed = entries[1][0]
    alarm = Alarm(hours, minutes, open, seconds_till_start, speed)
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
    global variableDict
    db = get_db()
    cursor = db.cursor()
    cur = cursor.execute('select value from settings')
    entries = cur.fetchall()
    time_value = entries[0][0]
    speed_value = entries[1][0]
    return render_template('settings.html', opened=variableDict['curtain_open'],
                           time_value=time_value, speed_value=speed_value)


@app.route('/change_settings', methods=['POST'])
def change_settings():
    time_value = int(request.form['time_before_start'])
    speed_value = int(request.form['speed'])
    db = get_db()
    cursor = db.cursor()
    cursor.execute('update settings set value = ? where id=1', (time_value,))
    cursor.execute('update settings set value = ? where id=2', (speed_value,))
    db.commit()
    return redirect(url_for('settings'))


@app.before_first_request
def start_job_thread():
    time_now = datetime.now()
    # Add old alarms to job queue
    db = get_db()
    cursor = db.cursor()
    cur = cursor.execute('select value from settings')
    entries = cur.fetchall()
    time_value = entries[0][0] * 60
    speed_value = entries[1][0]

    cur = cursor.execute('select id, hours, minutes, open from entries WHERE date >= '
                         + time_now.strftime("%Y-%m-%d") + ' AND done = 0 ORDER BY date, hours, minutes')

    for entry in cur.fetchall():
        hours = entry[1]
        minutes = entry[2]
        to_open = entry[3]
        alarm = Alarm(hours, minutes, to_open, time_value, speed_value)
        alarm.set_id(entry[0])

        curtain_job_controller_add(alarm)

    # Start worker thread
    t = threading.Thread(target=job_worker, daemon=True)
    t.start()


if __name__ == '__main__':
    app.run(use_reloader=False)

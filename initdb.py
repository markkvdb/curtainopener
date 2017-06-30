from flask import Flask, current_app

from curtainopener.database_handler import init_db
from curtainopener import app

with app.app_context():
    init_db()
    print('Database initialised.')
from flask import Flask

import os

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

import curtainopener.curtainopener
import curtainopener.database_handler
import curtainopener.functions
import curtainopener.stepcontroller
import curtainopener.alarm
import curtainopener.variables
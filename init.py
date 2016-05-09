import os.path
import flask
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
db = SQLAlchemy(app)

app.config.from_pyfile('settings.py')

recip_sockets = {}

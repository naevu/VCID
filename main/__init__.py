from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/sc-phoenix.db'
app.config['SECRET_KEY'] = '46qw87esad435asdqw87e6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
EVENT_TYPES = ["Training", "Match", "Tournament"]
USER_ROLES = ["ADMIN", "NORMAL"]

from main import routes
from main import api

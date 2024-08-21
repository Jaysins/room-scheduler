from flask_restful import Api
from flask import Flask
from .setup import ensure_default_room
from .models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)

# Create the database and tables
with app.app_context():
    db.create_all()
    ensure_default_room()

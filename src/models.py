"""
models.py

Data model file for application. This will connect to the mongo database and provide a source for storage
for the application service

"""

from datetime import datetime, timedelta
import json

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    appointments = db.relationship('Appointment', backref='customer', lazy=True)

    def __repr__(self):
        return f'<Customer {self.name}>'


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)
    number = db.Column(db.String(10), unique=True, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=True)
    appointments = db.relationship('Appointment', backref='room', lazy=True)

    def __repr__(self):
        return f'<Room {self.room_number}>'


# Appointment Model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='scheduled')

    def __repr__(self):
        return f'<Appointment {self.id}>'

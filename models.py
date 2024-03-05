from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50))
    axle = db.Column(db.String(50))
    year = db.Column(db.String(10))
    price = db.Column(db.String(20))
    color = db.Column(db.String(20))
    weight = db.Column(db.String(20))
    mileage = db.Column(db.String(20))
    photo = db.Column(db.String(100))
    description = db.Column(db.Text)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
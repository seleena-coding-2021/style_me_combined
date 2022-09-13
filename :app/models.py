from flask_login import UserMixin
from app import app, db



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    zipcode = db.Column(db.String(100))
    birthday = db.Column(db.String(100))

class Style(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(100), unique=True, nullable=False)
    stylechoice = db.Column(db.String(100))
    season = db.Column(db.String(100))
    #age_range = db.Column(db.String(100))
    #designer = db.Column(db.String(100))
    

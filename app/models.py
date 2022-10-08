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
    #age_range = db.Column(db.String(100))  #should this be left out again? (10/22)
    #designer = db.Column(db.String(100))   #should this be left out again (10/22)


# whenever things are added to this py file make sure: (10/22)
    # flask db stamp head
    # flask db migrate -m ""     (10/22)
    # flask db upgrade        (10/22)
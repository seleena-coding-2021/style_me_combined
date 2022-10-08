from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#from routes import routes   #not sure if this is needed (10/22)
from flask_migrate import Migrate
from config import Config


db = SQLAlchemy() #your database object 
migrate = Migrate() #migration engine #needed for migration (10/22)
login_manager = LoginManager() # Create a Login Manager instance
login_manager.login_view = 'auth.login' # define the redirection    
                         # path when login required and we attempt 
                         # to access without being logged in

 # The login manager contains the code that lets your application    
    # and Flask-Login work together

#def create_app(config_class=Config):  #should we try to include (10/22)
app = Flask(__name__) # creates the Flask instance, __name__ is the name of the current Python module
app.config.from_object(Config) #enable database config items

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app) # configure it for login


from app.models import User  #need app.models (10/22)
@login_manager.user_loader
def load_user(user_id): #reload user object from the user ID 
                            #stored in the session
        # since the user_id is just the primary key of our user 
        # table, use it in the query for the user
    return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    # blueprint allow you to orgnize your flask app
    #from auth import auth as auth_blueprint
    #app.register_blueprint(auth_blueprint)
    # blueprint for non-auth parts of app
    #from routes_styleme import styleme as styleme_blueprint
    #app.register_blueprint(styleme_blueprint)

    #return app

from app import routes, models  #importing models defines structure of db     routes?

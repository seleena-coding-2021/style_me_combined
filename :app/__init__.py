from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from routes_styleme import routes
from flask_migrate import Migrate
from config import Config


app = Flask(__name__) # creates the Flask instance, __name__ is the name of the current Python module
app.config.from_object(Config) #enable database config items
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
    
    # The login manager contains the code that lets your application    
    # and Flask-Login work together
    login_manager = LoginManager() # Create a Login Manager instance
    login_manager.login_view = 'auth.login' # define the redirection 
                         # path when login required and we attempt 
                         # to access without being logged in

    login_manager.init_app(app) # configure it for login
    from models import User
    @login_manager.user_loader
    def load_user(user_id): #reload user object from the user ID 
                            #stored in the session
        # since the user_id is just the primary key of our user 
        # table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    # blueprint allow you to orgnize your flask app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    # blueprint for non-auth parts of app
    #from routes_styleme import styleme as styleme_blueprint
    #app.register_blueprint(styleme_blueprint)

    return app

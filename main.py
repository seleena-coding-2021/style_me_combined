###############          Import packages         ###################

from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from __init__ import create_app, db


# our main blueprint
main = Blueprint('main', __name__)

@main.route('/login') # home page that return 'index'
def index():
   # return 'index' #returning the string 'index'
   return render_template('login.html') #grabs the html file 


@main.route('/profile') # profile page that return 'profile'
@login_required #requires you to login before you can do anything
def profile():
    #return 'profile' #returning the string 'profile'
    return render_template('profile.html', name=current_user.name)


app = create_app() # we initialize our flask app using the            
                   #__init__.py function

if __name__ == '__main__':
    db.create_all(app=create_app()) # create the SQLite database
    app.run(debug=False) # run the flask app on debug mode

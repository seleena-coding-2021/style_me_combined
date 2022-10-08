#from flask import Blueprint, Flask, render_template
#from flask_login import login_required, current_user
#from __init__ import create_app , db
#from app import create_app

# is only used to run the app



#app = create_app() # we initialize our flask app using the            
                   #__init__.py function

#if __name__ == '__main__':
  #  app.run(debug=False) # run the flask app on debug mode


#sources:

    #https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
    #https://medium.com/analytics-vidhya/creating-login-page-on-flask-9d20738d9f42 -- login page
    #https://stackoverflow.com/questions/32032504/python-time-greeting-program -- time greeting
    #https://www.w3schools.com/tags/att_input_required.asp -- required fields
    #https://docs.google.com/document/d/1aDFaB-ub7nm6bHMH5CCzXjMUMrVbt2M0cCsZbWAjwc4/edit?usp=sharing -- move code from local to github to pythonanywhere

from app import app

if __name__ == '__main__':
    app.run(debug=False)

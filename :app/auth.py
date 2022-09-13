######################          Import packages      ###################################

from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db


auth = Blueprint('auth', __name__) # create a Blueprint object that we name 'auth'

@auth.route('/adminstration')
@login_required
def admin():
    return render_template('adminstration.html')

@auth.route('/login', methods=['GET', 'POST']) # define login page path
def login(): # define login page fucntion
    if request.method=='GET': # if the request is a GET we return the login page
        return render_template('home.html')
    else: # if the request is POST the we check if the user exist and with te right password
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()
        hour = request.form.get('hour')   #get the time based on where the user is 
        print("the time is ... ", hour)    
        print("the type of hour is", type(hour))
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user:
            flash('Please sign up before!') #this does not work
            return redirect(url_for('auth.signup'))
        elif not check_password_hash(user.password, password):
            flash('Please check your login details and try again.') #this does not work
            return redirect(url_for('welcome')) # if the user doesn't exist or password is wrong, reload the page
        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        #return redirect(url_for('main.profile'))
        return redirect(url_for('choice', hour = hour))

@auth.route('/signup', methods=['GET', 'POST'])# we define the sign up path
def signup(): # define the sign up function
    if request.method=='GET': # If the request is GET we return the sign up page and forms
        return render_template('signup.html')
    else: # if the request is POST, then we check if the email doesn't already exist and then we save data
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        zipcode = request.form.get('zipcode')
        birthday = request.form.get('birthday')
        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists') #this does not work
            return redirect(url_for('auth.signup'))
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email,
                        name=name,
                        password=generate_password_hash(password, method='sha256'),
                        zipcode=zipcode,
                        birthday=birthday) #
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()   #commit all of the categories into the database
        return redirect(url_for('welcome'))

@auth.route('/profile') # profile page that return 'profile'
@login_required #requires you to login before you can do anything
def profile():
    #return 'profile' #returning the string 'profile'
    return render_template('profile.html', name=current_user.name, email=current_user.email, zipcode=current_user.zipcode, birthday=current_user.birthday)

@auth.route('/name_edit', methods=['GET', 'POST']) #edit your name
@login_required
def name_edit():
    if request.method=='GET':
        return render_template('editname.html', name=current_user.name)
    else:
        user=User.query.filter_by(email=current_user.email).first()
        user.name= request.form.get('name')
        db.session.commit()
    return redirect(url_for('auth.profile'))

@auth.route('/zipcode_edit', methods=['GET', 'POST'])  #edit your zip code
@login_required
def zipcode_edit():
    if request.method=='GET':
        return render_template('zipcodeedit.html', zipcode=current_user.zipcode)
    else:
        user=User.query.filter_by(email=current_user.email).first()
        user.zipcode= request.form.get('zipcode')
        db.session.commit()
    return redirect(url_for('auth.profile'))

@auth.route('/birthday_edit', methods=['GET', 'POST'])  #edit your birthday
@login_required
def birthday_edit():
    if request.method=='GET':
        return render_template('birthdayedit.html', birthday=current_user.birthday)
    else:
        user=User.query.filter_by(email=current_user.email).first()
        user.birthday= request.form.get('birthday')
        db.session.commit()
    return redirect(url_for('auth.profile'))
        
@auth.route('/logout') # define logout path
@login_required
def logout(): #define the logout function
    logout_user()
    return redirect(url_for('welcome'))

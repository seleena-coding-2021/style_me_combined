import requests
import configparser
from flask import render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db


#define style setting
style = "sporty"    #casual, sporty, dressy

def routes(app):
    # welcome page with login
    route('/')
    def welcome():
       return render_template("home.html")
    
    route('/stylechoice')
    def choice():
        hour = request.args.get('hour')
        hour = int(hour)
        if hour < 12:                   #https://stackoverflow.com/questions/32032504/python-time-greeting-program
            greeting = "Good Morning"
        elif hour < 18:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Night"
        return render_template("stylechoice.html", name=current_user.name, zipcode=current_user.zipcode, greet=greeting)

    #asks for zipcode of the city you are in
    route('/weather', methods=['POST'])
    def weather_dashboard():
        global style
        style = request.form['style']
        print(style)
        return render_template('location.html', zipcode=current_user.zipcode)

    # returns the weather and what it feels like
    route('/render_results', methods=['POST'])
    def render_results():
        style = request.form['style']
        print(style)
        zip_code=current_user.zipcode
        #zip_code = request.form['zipCode']
        print("Zip=",zip_code) #new code: not apart of the original
        # api_key = get_api_key()
        api_key = "f740a1fa30a15499826774d4c6ae2099"
        print("API KEY=",api_key) #new code: not apart of the original
        data = get_weather_results(zip_code, api_key)

        temp = "{0:.2f}".format(data["main"]["temp"])  #the main temp
        print("temperature is" + temp)
        feels_like = "{0:.2f}".format(data["main"]["feels_like"]) #feels like temp
        print ("feels like" + feels_like)
        weather = data["weather"][0]["main"]
        print ("weather is" + weather)
        location = data["name"] # name of the city where the user is
        print ("this is the location" + location)

        temp = float(temp)  # changing temp from an string into a float(intergers with decimals)
        print(style + " as in results")
        if style == "sporty":
          if temp<=40:
             return render_template('sporty_winter.html', location=location, temp=temp,
                           feels_like=feels_like, weather=weather)
          elif temp>40 and temp<=60:
             return render_template('sporty_early_spring.html', location=location, temp=temp,
                           feels_like=feels_like, weather=weather)
          elif temp>60 and temp<=80:
             return render_template('sporty_late_spring.html', location=location, temp=temp,
                           feels_like=feels_like, weather=weather)
          else:
             return render_template('sporty_summer.html', location=location, temp=temp,
                           feels_like=feels_like, weather=weather)
        elif style == "casual":
          if temp<=40:
             return render_template('casual_winter.html', location=location, temp=temp,
                           feels_like=feels_like, weather=weather)
          elif temp>40 and temp<=60:
             return render_template('casual_early_spring.html', location=location, temp=temp,
                           feels_like=feels_like, weather=weather)
          elif temp>60 and temp<=80:
             return render_template('casual_late_spring.html', location=location, temp=temp,
                           feels_like=feels_like, weather=weather)
          else:
              return render_template('casual_summer.html', location=location, temp=temp,
                             feels_like=feels_like, weather=weather)
        elif style == "dressy":
           if temp<=40:
              return render_template('dressy_winter.html', location=location, temp=temp,
                           feels_like=feels_like, weather=weather)
           elif temp>40 and temp<=60:
              return render_template('dressy_early_spring.html', location=location, temp=temp,
                           feels_like=feels_like, weather=weather)
           elif temp>60 and temp<=80:
              return render_template('dressy_late_spring.html', location=location, temp=temp,
                           feels_like=feels_like, weather=weather)
           else:
              return render_template('dressy_summer.html', location=location, temp=temp,
                             feels_like=feels_like, weather=weather)

    #def get_api_key():
       #config = configparser.ConfigParser()
       #config.read('config.ini')
       #print ("config=", config.sections())
       #return config['openweathermap']['api']

    def get_weather_results(zip_code, api_key):
       api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
       print(api_url)  #new code: not apart of the original
       r = requests.get(api_url)
       print(r)   #new code: not apart of the original
       return r.json()

###### below is from auth.py ################

route('/adminstration')
@login_required
def admin():
    return render_template('adminstration.html')

route('/login', methods=['GET', 'POST']) # define login page path
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
            return redirect(url_for('signup'))
        elif not check_password_hash(user.password, password):
            flash('Please check your login details and try again.') #this does not work
            return redirect(url_for('welcome')) # if the user doesn't exist or password is wrong, reload the page
        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        #return redirect(url_for('main.profile'))
        return redirect(url_for('choice', hour = hour))

route('/signup', methods=['GET', 'POST'])# we define the sign up path
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
            return redirect(url_for('signup'))
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

route('/profile') # profile page that return 'profile'
@login_required #requires you to login before you can do anything
def profile():
    #return 'profile' #returning the string 'profile'
    return render_template('profile.html', name=current_user.name, email=current_user.email, zipcode=current_user.zipcode, birthday=current_user.birthday)

route('/name_edit', methods=['GET', 'POST']) #edit your name
@login_required
def name_edit():
    if request.method=='GET':
        return render_template('editname.html', name=current_user.name)
    else:
        user=User.query.filter_by(email=current_user.email).first()
        user.name= request.form.get('name')
        db.session.commit()
    return redirect(url_for('profile'))

route('/zipcode_edit', methods=['GET', 'POST'])  #edit your zip code
@login_required
def zipcode_edit():
    if request.method=='GET':
        return render_template('zipcodeedit.html', zipcode=current_user.zipcode)
    else:
        user=User.query.filter_by(email=current_user.email).first()
        user.zipcode= request.form.get('zipcode')
        db.session.commit()
    return redirect(url_for('profile'))

route('/birthday_edit', methods=['GET', 'POST'])  #edit your birthday
@login_required
def birthday_edit():
    if request.method=='GET':
        return render_template('birthdayedit.html', birthday=current_user.birthday)
    else:
        user=User.query.filter_by(email=current_user.email).first()
        user.birthday= request.form.get('birthday')
        db.session.commit()
    return redirect(url_for('profile'))
        
route('/logout') # define logout path
@login_required
def logout(): #define the logout function
    logout_user()
    return redirect(url_for('welcome'))

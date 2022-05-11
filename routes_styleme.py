# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request
from flask_login import current_user
import requests
import configparser
import datetime
#from auth import hour

#app = Flask(__name__) ~ init is creating the app
#app.debug = True #don't like it

#define style setting
style = "sporty"    #casual, sporty, dressy


def routes(app):
    # welcome page with login
    @app.route('/')
    def welcome():
       return render_template("home.html")
    
    @app.route('/stylechoice')
    def choice():
        hour = request.args.get('hour')
        hour = int(hour)
        if hour < 12:
            greeting = "Good Morning"
        elif hour < 18:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Night"
        return render_template("stylechoice.html", name=current_user.name, zipcode=current_user.zipcode, greet=greeting)

    #asks for zipcode of the city you are in
    @app.route('/weather', methods=['POST'])
    def weather_dashboard():
        global style
        style = request.form['style']
        print(style)
        return render_template('location.html', zipcode=current_user.zipcode)

    # returns the weather and what it feels like
    @app.route('/render_results', methods=['POST'])
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
  #return render_template('results.html',
                           #location=location, temp=temp,
                           #feels_like=feels_like, weather=weather)

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

    def get_api_key():
       config = configparser.ConfigParser()
       config.read('config.ini')
       print ("config=", config.sections())
       return config['openweathermap']['api']

    def get_weather_results(zip_code, api_key):
       api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
       print(api_url)  #new code: not apart of the original
       r = requests.get(api_url)
       print(r)   #new code: not apart of the original
       return r.json()


#always goes last, but not needed in pythonanywhere
#if __name__ == "__main__":
    #app.run(debug=False) # run the flask app on debug mode
    


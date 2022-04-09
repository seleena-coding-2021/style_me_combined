import PySimpleGUI as sg
import requests

api_key = "f740a1fa30a15499826774d4c6ae2099"

def get_weather_results(zip_code, api_key):
       api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
       print(api_url)  #new code: not apart of the original
       r = requests.get(api_url)
       print(r)   #new code: not apart of the original
       return r.json()

def results(data):
       temp = "{0:.2f}".format(data["main"]["temp"])  #the main temp
       print("temperature is" + temp)
       feels_like = "{0:.2f}".format(data["main"]["feels_like"]) #feels like temp
       print ("feels like" + feels_like)
       weather = data["weather"][0]["main"]
       print ("weather is" + weather)
       location = data["name"] # name of the city where the user is
       print ("this is the location" + location)

       results = ('Weather in ' + location +
                  ' Temperature Today is '  + temp +
                  ' It Feels Like ' + feels_like+
                  weather)

       temp = float(temp)  # changing temp from an string into a float(intergers with decimals)

       if temp<=40:
              sg.popup('You should wear', title='Results', image=('casual_winter.png'))
       elif temp>40 and temp<=60:
              sg.popup('You should wear', title='Results', image=('casual_earlyspring.png'))
       elif temp>60 and temp<=80:
              sg.popup('You should wear', title='Results', image=('casual_latespring.png'))
       else:
              sg.popup('You should wear', title='Results', image=('casual_summer.png'))

       return(results)


sg.theme('TealMono')


layout = [[sg.Text('Style Me')],     #row 1, heading
          [sg.Text('the weather app that styles you')],    #row 2, slogan
          [sg.Text('Enter your zipcode')],      # row 3, user prompt
          [sg.Input()],          #row 4, input field
          [sg.Submit(), sg.Cancel()] ]    #row 5, Submit Button


# creating a window -- homepage

window = sg.Window('Style Me', layout)

event, values = window.read()
window.close ()

zipcode = values[0]
text_input = get_weather_results(zipcode, api_key)
print(text_input)
results = results(text_input)

sg.popup('Your zicope is', zipcode)
sg.popup('Weather Results', results)










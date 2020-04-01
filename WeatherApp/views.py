import requests
from django.shortcuts import render
from .models import city
# from pyrebase import pyrebase
from django.contrib import messages



# firebaseConfig = {
#     'apiKey': "AIzaSyCfLdUa2Gh65xTO_q1ESs30bWrlASdjAw0",
#     'authDomain': "weather-247ba.firebaseapp.com",
#     'databaseURL': "https://weather-247ba.firebaseio.com",
#     'projectId': "weather-247ba",
#     'storageBucket': "weather-247ba.appspot.com",
#     'messagingSenderId': "312320080238",
#     'appId': "1:312320080238:web:cc15e634870f55bbc6297f",
#     'measurementId': "G-M23C5E9BWH"
# }
#
# firebase = pyrebase.initialize_app(firebaseConfig)
# auth = firebase.auth()


# Getting City Weather Report By Using Api
def city_weather(request):
    #Url with api ky and city
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='
    if request.method == 'POST':
        status = True
        # TODO : If a city is already addd to the list don't add it again(UNIQUE) constraint will b voliated
        cities = city.objects.all()
        for i in cities:
            print(i)
            if i == request.POST['city']:
                status = False
                messages.info(request,'City Is Already Added')
                break
        if status:
            city_name = city()
            city_name.name = request.POST['city']
            city_name.save()

    weather_data = []
    cities = city.objects.all()
    for city_name in cities:
        response = requests.get(url.format(city_name))
        report = response.json()
        City_Weather = {
            'City': report['name'],
            'Temperature': report['main']['temp'],
            'Description': report['weather'][0]['description'],
            'Icon': report['weather'][0]['icon']
        }
        weather_data.append(City_Weather)
    #print(weather_data)
    return render(request, 'report.html', {"weather_data": weather_data})
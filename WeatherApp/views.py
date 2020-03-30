import requests
from django.shortcuts import render
from pyrebase import pyrebase
import json
from django.http import JsonResponse


firebaseConfig = {
    'apiKey': "AIzaSyCfLdUa2Gh65xTO_q1ESs30bWrlASdjAw0",
    'authDomain': "weather-247ba.firebaseapp.com",
    'databaseURL': "https://weather-247ba.firebaseio.com",
    'projectId': "weather-247ba",
    'storageBucket': "weather-247ba.appspot.com",
    'messagingSenderId': "312320080238",
    'appId': "1:312320080238:web:cc15e634870f55bbc6297f",
    'measurementId': "G-M23C5E9BWH"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


# Home Page
def home(request):
    return render(request, 'main.html')


# Getting City Weather Report By Using Api
def city_weather(request):
    # api key
    api_key = "bc94bea8e06b9bc36a7e9c46b6cda681"
    # api url
    base_url = "https://api.openweathermap.org/data/2.5/weather?q="

    if request.method == 'POST':
        city = request.POST['city']
        response = requests.get(base_url +  'LasVegas&units=metric&appid=' + api_key)
        report = response.json()

        print(report)
        City_Weather = {
            'City' : report['name'],
            'Temperature' : report['main']['temp'],
            'Description' : report['weather'][0]['description'],
            'Icon' : report['weather'][0]['icon']
        }
        return render(request, 'report.html', {"city_weather": City_Weather})
        #return JsonResponse(City_Weather,safe=False)

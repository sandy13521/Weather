import requests
from django.shortcuts import render, redirect
from .models import city
from django.contrib import messages

# Getting City Weather Report By Using Api
def city_weather(request):

    #Url with api ky and city
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=bc94bea8e06b9bc36a7e9c46b6cda681'
    if request.method == 'POST' :
        city_requested = request.POST['city']
        print(city.objects.filter(name = city_requested).count())
        err_msg = ""
        if city.objects.filter(name = city_requested).count() == 0 :
            r = requests.get(url.format(city_requested))
            report = r.json()
            if report['cod'] == 200:
                city_name = city()
                city_name.name = city_requested
                city_name.save()
            else:
                err_msg = "Invalid City Entered!!"
                messages.error(request,err_msg)
        else:
            err_msg = "City Is Already Exists."
            messages.error(request, err_msg)

        if err_msg == "":
            messages.success(request,"City is Succssfully Added.")


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
    return render(request, 'report.html', {"weather_data": weather_data})


# Method to Delete City From Database
def delete(request,city_name):
    try:
        city.objects.get(name = city_name).delete()
    finally:
        return redirect('/city')


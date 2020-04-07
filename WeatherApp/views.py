import requests
from django.shortcuts import render, redirect
from .models import city
from django.utils import timezone

# Url with api ky and city
url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='


# To convert Description to Upper Case
def upper_case(s):
    s = s.split()
    for i in range(len(s)):
        s[i] = s[i].capitalize()
    s = " ".join(s)
    return s


# Getting City Weather Report By Using Api
def city_weather_report(request):
    global url
    message = ''
    message_class = ''
    if request.method == 'POST':
        city_requested = request.POST['city']
        r = requests.get(url.format(city_requested))
        report = r.json()
        if report['cod'] == 200:
            if city.objects.filter(name=city_requested).count() == 0:
                city_name = city()
                city_name.name = report['name']
                city_name.time = timezone.now()
                city_name.temp = report['main']['temp']
                city_name.des = upper_case(report['weather'][0]['description'])
                city_name.icon = report['weather'][0]['icon']
                city_name.save()
                message = "City Successfully Added"
                message_class = 'is-success'
            else:
                message = "Already Exists"
                message_class = 'is-danger'
        else:
            message = "Invalid City"
            message_class = 'is-danger'

    weather_data = []
    cities = city.objects.all()
    current_time = timezone.now()

    for i in range(len(cities)):
        last_updated_time = cities[i].time
        diff = current_time - last_updated_time
        if diff.total_seconds() < 3600:
            city_weather = {
                'City': cities[i].name,
                'Temperature': cities[i].temp,
                'Description': cities[i].des,
                'Icon': cities[i].icon,
                'Last_Updated': last_updated_time
            }
            weather_data.append(city_weather)
        else:
            response = requests.get(url.format(cities[i].name))
            report = response.json()
            to_be_changed = report['weather'][0]['description']
            des = upper_case(to_be_changed)

            # Updating into Database
            update_city = city.objects.get(name=cities[i].name)
            update_city.time = timezone.now()
            update_city.temp = report['main']['temp']
            update_city.des = upper_case(report['weather'][0]['description'])
            update_city.icon = report['weather'][0]['icon']
            update_city.save()

            city_weather = {
                'City': report['name'],
                'Temperature': report['main']['temp'],
                'Description': des,
                'Icon': report['weather'][0]['icon'],
                'Last_Updated': timezone.now()
            }
            weather_data.append(city_weather)

    context = {
        "weather_data": weather_data,
        "message": message,
        "message_class": message_class
    }
    return render(request, 'report.html', context)


# Method to Delete City From Database
def delete(request, city_name):
    try:
        city.objects.get(name=city_name).delete()
    finally:
        return redirect('/city')


# To refresh the data in database
def refresh(request, city_name):
    response = requests.get(url.format(city_name))
    report = response.json()
    update_city = city.objects.get(name=city_name)
    update_city.time = timezone.now()
    update_city.temp = report['main']['temp']

    update_city.des = upper_case(report['weather'][0]['description'])
    update_city.icon = report['weather'][0]['icon']
    update_city.save()
    return redirect("/city")

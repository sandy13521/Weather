from django.contrib import admin
from django.urls import path
from WeatherApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('city', city_weather_report),
    path('delete/<city_name>', delete),
    path('refresh/<city_name>', refresh)
]

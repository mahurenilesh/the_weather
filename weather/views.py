from django.core.checks.messages import Error
import requests
from django.shortcuts import render, redirect
from requests.sessions import Request
from .models import *
from .forms import *

# Create your views here.

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=6ab14b7af8895619889e87172ad54870'
    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existign_city_count = City.objects.filter(name=new_city).count()
            
            if existign_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                
                if r['cod'] == 200:
                    form.save()
                
                else:
                    err_msg = 'City does not exist in the world!'
            
            else:
                err_msg = 'City already exists in the database!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
                'city':city.name,
                'temperature': r['main']['temp'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    
    context = {
        'weather_data' : weather_data,
        'form' : form,
        "message" : message,
        'message_class' : message_class,
    }

    return render(request,
                  'weather/weather.html',
                  context)

def delete_city(request, city_name):
    City.objects.get(name = city_name).delete()
    return redirect('home')
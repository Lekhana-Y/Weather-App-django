from django.shortcuts import render, redirect
from .models import City
import requests

def index(request):

    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=834b5f328bdc2728a4085470da02a73d'

    error_message = ''

    if request.method == 'POST':

        if 'city' in request.POST:

            city = request.POST['city'].strip()

            if city != '':

                try:
                    response = requests.get(url.format(city), timeout=5).json()

                    if response.get('cod') == 200:

                        if not City.objects.filter(name__iexact=city).exists():
                            City.objects.create(name=city)

                    else:
                        error_message = "City not found!"

                except:
                    error_message = "Network error"


        if 'delete_city' in request.POST:

            City.objects.filter(name=request.POST['delete_city']).delete()


        return redirect('home')


    cities = City.objects.all()

    weather_data = []

    for city in cities:

        try:
            response = requests.get(url.format(city.name), timeout=5).json()

            if response.get('cod') == 200:

                city_weather = {
                    'city': city.name,
                    'temperature': response['main']['temp'],
                    'description': response['weather'][0]['description'],
                    'main': response['weather'][0]['main'],
                    'icon': response['weather'][0]['icon'],
                    'image': f'https://picsum.photos/400/300?random={city.name}'
                }

                weather_data.append(city_weather)

        except:
            continue


    context = {
        'weather_data': weather_data,
        'error': error_message
    }

    return render(request,'weather/index.html',context)
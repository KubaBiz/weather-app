from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core import serializers
from django.http import Http404, HttpResponseNotAllowed
import pandas as pd
import json

from .forms import LocationForm
from .weather_request import request_data


def start_view(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            request.session['latitude'] = str(latitude)
            request.session['longitude'] = str(longitude)

            return redirect('weather')
    else:
        form = LocationForm()
    return render(request, 'homepage/startpage.html', {'form': form})

def weather_view(request):
    latitude = float(request.session.get('latitude'))
    longitude = float(request.session.get('longitude'))
    weather_data = request_data(latitude, longitude)   
    if isinstance(weather_data, Exception):
        return HttpResponse(weather_data)
    weather_icons = {
        0: '<i class="fa-solid fa-sun" style="font-size:32px"></i>',
        1: '<i class="fa-solid fa-cloud-sun" style="font-size:32px"></i>',
        2: '<i class="fa-solid fa-cloud" style="font-size:32px"></i>',
        3: '<i class="fa-solid fa-smog" style="font-size:32px"></i>',
        4: '<i class="fa-solid fa-cloud-rain" style="font-size:32px"></i>',
        5: '<i class="fa-solid fa-icicles" style="font-size:32px"></i>',
        6: '<i class="fa-solid fa-cloud-showers-heavy" style="font-size:32px"></i>',
        7: '<i class="fa-solid fa-cloud-showers-water" style="font-size:32px"></i>',
        8: '<i class="fa-solid fa-snowflake" style="font-size:32px"></i>',
        9: '<i class="fa-solid fa-cloud-meatball" style="font-size:32px"></i>',
        10: '<i class="fa-solid fa-bolt-lightning" style="font-size:32px"></i>',
        11: '<i class="fa-solid fa-cloud-bolt" style="font-size:32px"></i>',
    }
    return render(request, 'homepage/weather.html', {'weather_data': weather_data, 'weather_icons': weather_icons})

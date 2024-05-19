from django.urls import path

from . import views

urlpatterns = [
    path('start/', views.start_view, name='location_input'),
    path('start/weather', views.weather_view, name='weather'),
]
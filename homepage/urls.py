from django.urls import path
from . import views


urlpatterns = [
    path('start/', views.start_view, name='start'),
    path('start/weather', views.weather_view, name='weather'),
]
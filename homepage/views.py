from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.http import Http404, HttpResponseNotAllowed
import json

# Create your views here.

def index(request):    return render(request, 'homepage/index.html', {})


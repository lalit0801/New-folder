from django.shortcuts import render
import json
import urllib.request

# Create your views here.
def index(request):
    return render(request, 'lobby.html')
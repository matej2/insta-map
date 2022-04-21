import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from photo.models import Photo

def infoView(request):
    return render(request, 'common/info.html')

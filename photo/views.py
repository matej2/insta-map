import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from photo.models import Photo

def photo_list(request):
    p = json.dumps(list(Photo.objects.values()))
    return HttpResponse(p, content_type="application/json")


def locationPhotoView(request):
    return render(request, 'example.html')

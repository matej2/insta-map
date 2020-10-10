# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import HttpResponse

# Create your views here.
from location.models import Location


def location_list(request):
    p = json.dumps(list(Location.objects.values()))
    return HttpResponse(p, content_type="application/json")

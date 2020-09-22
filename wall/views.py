# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.shortcuts import render
from insta_map.settings import BASE_DIR


# Create your views here.
def index_summary(request):
    return render(request, 'example.html', {})

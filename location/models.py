# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Location:
    def __init__(self, id, name):
        self.id = id
        self.name = name
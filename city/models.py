from django.db import models

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=255, null=True)
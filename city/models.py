from django.db import models

# Create your models here.


class City(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name
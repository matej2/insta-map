from itertools import chain

from django.db import models

# Create your models here.
from location.models import Location


class Photo(models.Model):
    thumbnail = models.CharField(max_length=255, null=True)
    caption = models.TextField(max_length=255, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def to_dict(instance):
        opts = instance._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            data[f.name] = f.value_from_object(instance)
        for f in opts.many_to_many:
            data[f.name] = [i.id for i in f.value_from_object(instance)]
        return data

    def __str__(self):
        return str('{}: {}'.format(self.id, self.caption[:20]))
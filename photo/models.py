from itertools import chain

from django.db import models


class Photo(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    thumbnail = models.CharField(max_length=500, null=True)
    caption = models.TextField(max_length=255, null=True)
    accessibility_caption = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255, null=True)

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
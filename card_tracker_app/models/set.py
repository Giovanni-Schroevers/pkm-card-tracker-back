from django.db import models
from . import Series


class Set(models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    series = models.ForeignKey(Series, models.SET_NULL, 'sets', null=True)

    def __str__(self):
        return self.name

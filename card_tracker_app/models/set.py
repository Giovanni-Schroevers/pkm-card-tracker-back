from django.db import models


class Set(models.Model):
    code = models.CharField(max_length=255, unique=False, null=True)
    name = models.CharField(max_length=255, unique=True)
    cards_per_row = models.IntegerField(default=3)

    def __str__(self):
        return self.name

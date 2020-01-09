from django.db import models


class Set(models.Model):
    code = models.CharField(max_length=255, unique=True, null=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

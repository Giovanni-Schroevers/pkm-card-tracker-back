from django.db import models
from . import Set


class Card(models.Model):
    name = models.CharField(max_length=255)
    card_number = models.IntegerField()
    set = models.ForeignKey(Set, models.CASCADE, 'cards')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('card_number', 'set')

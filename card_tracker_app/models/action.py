from django.db import models
from django_enumfield import enum

from . import Set, Card, User


class ActionTypes(enum.Enum):
    ADD = 0
    LOAN = 1


class Action(models.Model):
    action = enum.EnumField(ActionTypes, default=ActionTypes.ADD)
    user = models.ForeignKey(User, models.CASCADE, 'action_user')
    set = models.ForeignKey(Set, models.CASCADE, 'action_set')
    card = models.ForeignKey(Card, models.CASCADE, 'action_card')

    def __str__(self):
        return self.action

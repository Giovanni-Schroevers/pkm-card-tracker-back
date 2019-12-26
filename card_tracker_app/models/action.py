from django.db import models
from django.utils.timezone import now
from django_enumfield import enum

from . import Set, Card, User


class ActionTypes(enum.Enum):
    ADD = 0
    LOAN = 1


class Action(models.Model):
    action = enum.EnumField(ActionTypes, default=ActionTypes.ADD)
    created_at = models.DateTimeField(default=now, editable=False)
    user = models.ForeignKey(User, models.CASCADE, 'user_action')
    set = models.ForeignKey(Set, models.CASCADE, 'set_action')
    card = models.ForeignKey(Card, models.CASCADE, 'card_action')

    def __str__(self):
        return f"Action: {str(self.action)}, Card: {str(self.card)}, Date: {str(self.created_at)}"

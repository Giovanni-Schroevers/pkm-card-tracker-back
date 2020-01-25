from django.db import models

from card_tracker_app.models import User, Card


class CardOwned(models.Model):
    user = models.ForeignKey(User, models.CASCADE, 'user_card_owned')
    card = models.ForeignKey(Card, models.CASCADE, 'card_card_owned')
    is_loan = models.BooleanField(default=False)

    def __str__(self):
        return self.is_loan

    class Meta:
        db_table = "card_tracker_app_card_owned"

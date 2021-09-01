from django.db import models

from card_tracker_app.models import User, Card


class Comment(models.Model):
    user = models.ForeignKey(User, models.CASCADE, 'comments')
    card = models.ForeignKey(Card, models.CASCADE, 'comments')
    text = models.TextField()

    def __str__(self):
        return self.text

    class Meta:
        db_table = "card_tracker_app_comment"

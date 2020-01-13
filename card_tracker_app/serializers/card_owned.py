from rest_framework import serializers

from card_tracker_app.models import CardOwned


class CardOwnedSerializer(serializers.ModelSerializer):

    class Meta:
        model = CardOwned
        fields = (
            'id',
            'user',
            'card',
            'is_loan'
        )

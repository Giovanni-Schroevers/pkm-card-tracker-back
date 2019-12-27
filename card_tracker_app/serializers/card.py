from rest_framework import serializers

from card_tracker_app.models import Card


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = (
            'id',
            'name',
            'number',
            'set'
        )


class CardInSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = (
            'id',
            'name',
            'number',
        )

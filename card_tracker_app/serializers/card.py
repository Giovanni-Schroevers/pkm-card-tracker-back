from rest_framework import serializers

from card_tracker_app.models import Card


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = (
            'id',
            'name',
            'number',
            'set',
            'rarity'
        )


class CardInSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = (
            'id',
            'name',
            'number',
            'rarity',
        )


class CardSetOverviewSerializer(serializers.ModelSerializer):
    total_cards = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = (
            'number',
            'total_cards'
        )

    def get_total_cards(self, obj):
        cards_owned = obj.card_card_owned.all().count()
        return cards_owned

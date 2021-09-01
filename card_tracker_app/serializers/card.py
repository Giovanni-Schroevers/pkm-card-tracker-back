from rest_framework import serializers

from card_tracker_app.models import Card
from card_tracker_app.serializers.comment import CommentSerializer


class CardSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Card
        fields = (
            'id',
            'name',
            'number',
            'set',
            'rarity',
            'comments'
        )


class CardInSetSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Card
        fields = (
            'id',
            'name',
            'number',
            'rarity',
            'comments'
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

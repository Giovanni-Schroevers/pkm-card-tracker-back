import json

from rest_framework import serializers

from card_tracker_app.models import Set
from card_tracker_app.serializers.card import CardSetOverviewSerializer


class SetSerializer(serializers.ModelSerializer):
    # cards = serializers.SerializerMethodField(read_only=True)
    cards_per_row = serializers.IntegerField(read_only=True)

    class Meta:
        model = Set
        fields = (
            'id',
            'code',
            'name',
            'cards_per_row',
            # 'cards',
        )

    # def get_cards(self, obj):
    #     cards_owned = []
    #     cards = CardSetOverviewSerializer(obj.cards, many=True)
    #     for card in cards.data:
    #         json_card = json.loads(json.dumps(card))
    #         if json_card['total_cards'] > 0:
    #             print(json_card)
    #             cards_owned.append(json_card)
    #     return cards_owned

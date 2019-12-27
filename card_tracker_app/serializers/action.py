from rest_framework import serializers

from card_tracker_app.models import Action


class ActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = (
            'id',
            'action',
            'user',
            'card'
        )

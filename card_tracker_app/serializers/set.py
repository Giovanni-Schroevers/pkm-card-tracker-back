from rest_framework import serializers

from card_tracker_app.models import Set


class SetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Set
        fields = (
            'id',
            'code',
            'name',
        )

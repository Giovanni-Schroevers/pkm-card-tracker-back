from rest_framework import serializers

from card_tracker_app.models import Comment, User, Card
from card_tracker_app.serializers.user import UserOverviewSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserOverviewSerializer()

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'user'
        )


class CommentSaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'user',
            'card'
        )

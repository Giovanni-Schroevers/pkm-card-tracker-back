from rest_framework import serializers

from card_tracker_app.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'password',
            'email',
            'is_admin'
        )


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email',
            'is_admin'
        )


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255)

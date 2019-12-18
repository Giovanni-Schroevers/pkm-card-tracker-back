from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

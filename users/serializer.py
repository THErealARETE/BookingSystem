from rest_framework import serializers, validators
from .models import User


class TokenSerializer(serializers.Serializer):

    """  
    serializer for token data
    """
    # token = serializers.CharField(max_length = 255,  read_only=True)
    token = serializers.CharField(max_length = 255)


class UserSerializer(serializers.ModelSerializer):
    """
    serializer for the user object
    """
    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('id','username', 'first_name','last_name', 'email', 'password')


class UserLoginSerializer(serializers.ModelSerializer):
    """
    serializer for login object
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'password')


class ImageUploadSerializer(serializers.ModelSerializer):
    """
    serializer for image object
    """

    class Meta:
        model = User
        fields = ('id', 'photo', 'updated_at')
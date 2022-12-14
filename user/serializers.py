from rest_framework import serializers
from .models import User


class UserSerializer(serializers.Serializer):
    """
    User Serializer request and create new user
    """
    id = serializers.IntegerField(required=False)
    username = serializers.CharField(required=True)
    email = serializers.EmailField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    password = serializers.CharField(max_length=128, min_length=8, required=True, allow_null=False, allow_blank=False)
    is_verified = serializers.BooleanField(default=True)
    is_superuser=serializers.BooleanField(required=False,default=False)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)





    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.id = validated_data.get('id', instance.id)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.password = validated_data.get('password', instance.password)
        instance.is_verified = validated_data.get('is_verified', instance.is_verified)
        instance.save()
        return instance

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists!")
        return value

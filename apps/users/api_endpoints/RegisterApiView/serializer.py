from rest_framework import serializers
from django.utils import timezone
from apps.users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    def create(self, validated_data):
        user = User(
            email=validated_data['email'].lower(),
            username=validated_data['username'],
            full_name=validated_data.get('username')
        )
        user.set_password(validated_data['password'])
        user.date_joined = timezone.now()
        user.save()
        return user

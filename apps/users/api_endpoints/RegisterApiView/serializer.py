from rest_framework import serializers
from django.utils import timezone
from apps.users.models import User
import uuid
from apps.users.helpers import *


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password']

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    def create(self, validated_data):
        request = self.context.get("request")

        user = User(
            email=validated_data['email'].lower(),
            full_name=validated_data.get('full_name'),
            username=str(uuid.uuid4())[:30]

        )
        user.set_password(validated_data['password'])
        user.date_joined = timezone.now()
        user.save()
        if request:
            log_auth_action(
                user=user,
                action=AuthLog.ActionChoices.REGISTER,
                request=request,
                metadata={"info": "Foydalanuvchi ro‘yxatdan o‘tdi"}
            )

        return user

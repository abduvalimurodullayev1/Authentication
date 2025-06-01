from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import RefreshToken as RefreshTokenModel, AuthLog
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Email yoki parol noto‘g‘ri.")
        if not user.is_active:
            raise serializers.ValidationError("Foydalanuvchi aktiv emas.")
        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data['user']
        request = self.context.get('request')

        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        user_agent = request.headers.get('User-Agent', '')

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        RefreshTokenModel.objects.create(
            user=user,
            token=refresh_token,
            ip_address=ip,
            user_agent=user_agent,
            is_valid=True,
        )

        AuthLog.objects.create(
            user=user,
            action=AuthLog.ActionChoices.LOGIN,
            ip_address=ip,
            user_agent=user_agent,
            metadata={"Action": "Logged in"}
        )

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': 15 * 60,
        }

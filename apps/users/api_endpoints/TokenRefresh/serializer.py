from django.utils import timezone
from rest_framework import serializers
from apps.users.models import RefreshToken as RefreshTokenModel


class TokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        token = attrs.get('refresh_token')

        try:
            refresh_token_obj = RefreshTokenModel.objects.get(token=token, is_valid=True)
        except RefreshTokenModel.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired refresh token.")

        if refresh_token_obj.expires_at and refresh_token_obj.expires_at < timezone.now():
            refresh_token_obj.is_valid = False
            refresh_token_obj.save()
            raise serializers.ValidationError("Refresh token expired.")

        attrs['refresh_token_obj'] = refresh_token_obj
        attrs['user'] = refresh_token_obj.user
        return attrs

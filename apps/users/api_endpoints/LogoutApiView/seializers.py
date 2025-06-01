from rest_framework import serializers
from apps.users.models import RefreshToken


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    def validate_refresh_token(self, value):
        try:
            RefreshToken(value)
        except Exception:
            raise serializers.ValidationError("Noto'g'ri refresh token.")
        return value

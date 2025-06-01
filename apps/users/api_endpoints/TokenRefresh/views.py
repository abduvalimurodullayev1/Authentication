from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from apps.users.models import RefreshToken as RefreshTokenModel
from rest_framework.permissions import AllowAny
from django.utils import timezone


class RefreshTokenAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        old_refresh_token = request.data.get('refresh_token')

        if not old_refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token_obj = RefreshTokenModel.objects.get(token=old_refresh_token, is_valid=True)
        except RefreshTokenModel.DoesNotExist:
            return Response({"detail": "Invalid or expired refresh token."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            token = RefreshToken(old_refresh_token)
        except TokenError:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_401_UNAUTHORIZED)

        user = token_obj.user

        token_obj.is_valid = False
        token_obj.invalidated_at = timezone.now()
        token_obj.save()
        new_refresh = RefreshToken.for_user(user)
        new_refresh_token = str(new_refresh)
        new_access_token = str(new_refresh.access_token)

        RefreshTokenModel.objects.create(
            user=user,
            token=new_refresh_token,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.headers.get('User-Agent', ''),
            is_valid=True,
        )

        return Response({
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "Bearer",
            "expires_in": 15 * 60,
        }, status=status.HTTP_200_OK)

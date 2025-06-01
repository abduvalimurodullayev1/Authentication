from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError

from apps.users.helpers import log_auth_action
from apps.users.models import RefreshToken as RefreshTokenModel, AuthLog
from apps.users.api_endpoints.LogoutApiView.seializers import LogoutSerializer


class LogoutAPIView(CreateAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        refresh_token = serializer.validated_data['refresh_token']
        user = self.request.user

        try:
            token_obj = RefreshTokenModel.objects.get(
                token=refresh_token, user=user, is_valid=True
            )
            token_obj.delete()
        except RefreshTokenModel.DoesNotExist:
            raise ValidationError("Token topilmadi yoki allaqachon bekor qilingan.")

        log_auth_action(
            user=user,
            action=AuthLog.ActionChoices.LOGOUT,
            request=self.request,
            metadata={"action": "User logged out"}
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"detail": "Muvaffaqiyatli logout qilindi."}, status=status.HTTP_200_OK)

__all__ = ['LogoutAPIView']
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from apps.users.models import RefreshToken as RefreshTokenModel
from apps.users.api_endpoints.LogoutApiView.seializers import LogoutSerializer
from apps.users.models import AuthLog


class LogoutAPIView(CreateAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        refresh_token = serializer.validated_data['refresh_token']
        user = self.request.user

        try:
            token_obj = RefreshTokenModel.objects.get(token=refresh_token, user=user, is_valid=True)
            token_obj.delete()
        except RefreshTokenModel.DoesNotExist:
            raise ValidationError("Token topilmadi yoki allaqachon bekor qilingan.")

        request = self.request
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        user_agent = request.headers.get('User-Agent', '')

        AuthLog.objects.create(
            user=user,
            action=AuthLog.ActionChoices.LOGOUT,
            ip_address=ip,
            user_agent=user_agent,
            metadata={"Action": "Logged out"}
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"detail": "Muvaffaqiyatli logout qilindi."}, status=status.HTTP_200_OK)

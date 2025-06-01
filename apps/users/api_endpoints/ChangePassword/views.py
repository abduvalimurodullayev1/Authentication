# apps/users/api_endpoints/ChangePassword/views.py

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import update_session_auth_hash

from apps.users.models import RefreshToken, AuthLog
from apps.users.api_endpoints.ChangePassword.serializers import ChangePasswordSerializer
from apps.users.helpers import *


class ChangePasswordAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(old_password):
                return Response(
                    {"old_password": ["Eski parol noto‘g‘ri"]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(new_password)
            user.save()

            RefreshToken.objects.filter(user=user, is_valid=True).update(is_valid=False)

            update_session_auth_hash(request, user)

            log_auth_action(
                user=user,
                action=AuthLog.ActionChoices.PASSWORDCHANGE,
                request=request,
                metadata={"info": "Parol o‘zgartirildi"}
            )

            return Response(
                {"detail": "Parol muvaffaqiyatli o‘zgartirildi"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


__all__ = ['ChangePasswordAPIView']

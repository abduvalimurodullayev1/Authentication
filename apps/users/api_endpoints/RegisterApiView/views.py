from rest_framework.generics import CreateAPIView
from apps.users.api_endpoints.RegisterApiView.serializer import RegisterSerializer


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer


__all__ = ['RegisterAPIView']

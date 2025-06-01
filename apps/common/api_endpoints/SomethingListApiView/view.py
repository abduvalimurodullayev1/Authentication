from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.common.api_endpoints.SomethingListApiView.serializer import SomethingSerializer
from apps.common.models import Something


class SomethingListApiView(ListAPIView):
    serializer_class = SomethingSerializer
    queryset = Something.objects.all()
    permission_classes = [IsAuthenticated]


__all__ = ['SomethingListApiView']

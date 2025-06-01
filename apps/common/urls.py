from django.urls import path

from apps.common.api_endpoints.SomethingListApiView.view import SomethingListApiView

app_name = "common"
urlpatterns = [
    path("Something/", SomethingListApiView.as_view(), name="something")
]

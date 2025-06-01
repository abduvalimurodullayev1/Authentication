from django.urls import path

from apps.users.api_endpoints.LoginApiView.views import LoginAPIView
from apps.users.api_endpoints.LogoutApiView.views import LogoutAPIView
from apps.users.api_endpoints.RegisterApiView.views import RegisterAPIView
from apps.users.api_endpoints.TokenRefresh.views import RefreshTokenAPIView
from apps.users.views import AdminOnlyView, ManagerOrAdminView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("refresh/", RefreshTokenAPIView.as_view(), name="refresh-token"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path('admin-only/', AdminOnlyView.as_view(), name='admin-only'),
    path('manager-or-admin/', ManagerOrAdminView.as_view(), name='manager-or-admin'),
]

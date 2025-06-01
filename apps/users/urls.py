from django.urls import path
from apps.users import api_endpoints
from apps.users.views import AdminOnlyView, ManagerOrAdminView

urlpatterns = [
    path('register/', api_endpoints.RegisterAPIView.as_view(), name='register'),
    path("login/", api_endpoints.LoginAPIView.as_view(), name="login"),
    path("refresh/", api_endpoints.RefreshTokenAPIView.as_view(), name="refresh-token"),
    path("logout/", api_endpoints.LogoutAPIView.as_view(), name="logout"),
    path('admin-only/', AdminOnlyView.as_view(), name='admin-only'),
    path('manager-or-admin/', ManagerOrAdminView.as_view(), name='manager-or-admin'),
    path("change-password/", api_endpoints.ChangePasswordAPIView.as_view(), name="change-password")
]

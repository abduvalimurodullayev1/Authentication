from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from apps.common.models import BaseModel
from apps.users.manager import UserManager


class User(AbstractUser):
    class RoleChoice(models.TextChoices):
        MANAGER = 'manager', _('Manager')
        ADMIN = 'admin', _("Admin")
        USER = 'user', _("User")

    email = models.EmailField(unique=True, verbose_name=_("email"))
    full_name = models.CharField(max_length=255, verbose_name=_("full name"))
    role = models.CharField(max_length=20, choices=RoleChoice, default='user', verbose_name=_("role"))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class RefreshToken(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField(unique=True)
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField()
    replaced_by_token = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='replaced_tokens'
    )

    class Meta:
        unique_together = ('user', 'token')


class AuthLog(BaseModel):
    class ActionChoices(models.TextChoices):
        LOGIN = 'login', 'Login'
        LOGOUT = 'logout', 'Logout'
        REGISTER = 'register', 'Register'
        REFRESH = 'refresh', 'Refresh'
        PASSWORDCHANGE = 'password_change', 'Change Password'

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("user"))
    action = models.CharField(max_length=20, choices=ActionChoices.choices, verbose_name=_("action"))
    ip_address = models.GenericIPAddressField(verbose_name=_("ip address"), null=True, blank=True)
    user_agent = models.TextField(verbose_name=_("user agent"))
    metadata = models.JSONField(default=dict)

from django.contrib import admin

from apps.common.models import Something
from apps.users.models import User, RefreshToken, AuthLog


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "role", "full_name")
    list_display_links = ("id",)


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "updated_at")


@admin.register(AuthLog)
class AuthLogAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    list_display_links = ("id", "user")


admin.site.register(Something)

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The given phone must be set"))

        email = self.normalize_email(email)

        if self.model.objects.filter(email=email).exists():
            raise ValueError(_("A user with this phone number already exists"))

        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser is_staff=True bo'lishi kerak."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser is_superuser=True bo'lishi kerak."))
        if extra_fields.get("is_active") is not True:
            raise ValueError(_("Superuser is_active=True bo'lishi kerak."))

        return self._create_user(email, password, **extra_fields)

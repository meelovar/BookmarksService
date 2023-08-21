from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import gettext_lazy as _

from api_auth.models.managers import UserManager


class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()

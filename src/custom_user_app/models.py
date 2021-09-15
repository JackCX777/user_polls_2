from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy

# from django.contrib.auth.models import AbstractBaseUser
# from django.contrib.auth.models import PermissionsMixin
# from django.utils import timezone

from custom_user_app.managers import CustomUserManager


class User(AbstractUser):
    """
        Using AbstractUser (use this subclass if you are happy with the existing fields in the User model and just want
        to remove the username field):
        Create a new User class that is based on AbstractUser
        Remove the username field
        Make email mandatory and unique
        Set USERNAME_FIELD to define a unique identifier in the User model with the value of email
        Specify that all objects for the User class are from CustomUserManager
    """
    username = None
    email = models.EmailField(ugettext_lazy('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        # You can delete the db_table='auth_user' only after you have finished customising the user
        # and the last migration has been completed.

        db_table = 'auth_user'
        # pass

    def __str__(self):
        return self.email


# class User(AbstractBaseUser, PermissionsMixin):
#     """
#         Using AbstractBaseUser (use this subclass if you want to create your own, completely new User model
#         from scratch):
#         Create new User class based on AbstractBaseUser
#         Add fields email, is_staff, is_active, and date_joined
#         Set USERNAME_FIELD that defines unique identifier for the User model with the value email
#         Specify that objects for the User class are from CustomUserManager
#     """
#     email = models.EmailField(ugettext_lazy('email address'), unique=True)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     date_joined = models.DateTimeField(default=timezone.now)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#     objects = CustomUserManager()
#
#     class Meta:
#         db_table = 'auth_user'
#
#     def __str__(self):
#         return self.email

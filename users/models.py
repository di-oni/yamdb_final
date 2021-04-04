from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    """Custom model of roles in app."""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    """Expansion of user functionality. Inherited from AbstractUser."""
    bio = models.TextField(blank=True, default='')
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER
    )
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=150, unique=False, default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_admin(self):
        return self.role == Role.ADMIN

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR

    @property
    def is_user(self):
        return self.role == Role.USER

from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField('email', max_length=254, unique=True)
    username = models.CharField('username', max_length=150)
    first_name = models.CharField('first_name', max_length=150)
    last_name = models.CharField('last_name', max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name'
    ]

    objects = CustomUserManager()

    def __str__(self):
        return self.username

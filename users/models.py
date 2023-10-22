from django.db import models
from django.contrib.auth.models import AbstractUser


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    avatar = models.ImageField(
        upload_to='users/',
        **NULLABLE,
        verbose_name='Аватар'
    )
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    code = models.CharField(
        max_length=8,
        verbose_name='Код подтверждения',
        **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

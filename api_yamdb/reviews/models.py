from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = [
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор')
]


class User(AbstractUser):

    email = models.EmailField(
        max_length=50,
        unique=True,
        blank=False
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True
    )
    role = models.CharField(
        max_length=24,
        verbose_name='Роль',
        choices=ROLES,
        default='user'
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default='XXXX'
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь',

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return (
            self.role == ADMIN
            or self.is_superuser
        )


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

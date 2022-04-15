from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.conf import settings


class MyUser(AbstractUser):
    refresh_token = models.TextField(
        verbose_name='Refresh Token', blank=True, null=True)


def used_timedelta():
    return timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']


class MyToken(Token):
    key = models.CharField("Key", max_length=255, primary_key=True)
    user = models.OneToOneField(
        MyUser, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name="User"
    )
    used_time = models.DateTimeField(
        verbose_name='Used Time',
        default=used_timedelta,
        blank=True, null=True)

    def is_expired(self):
        is_expired = timezone.now().timestamp() > self.used_time.timestamp()
        return is_expired

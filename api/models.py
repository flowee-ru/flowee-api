import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator


class User(AbstractUser):
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(r'^[a-zA-Z0-9_]*$')],
        error_messages={
            'unique': 'A user with that username already exists.'
        }
    )
    password = models.CharField(max_length=100, validators=[MinLengthValidator(6)])
    display_name = models.CharField(max_length=30, null=True)
    bio = models.TextField(max_length=500, null=True)
    live_name = models.CharField(max_length=30, null=True)
    live_key = models.UUIDField(default=uuid.uuid4)

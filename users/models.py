from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    # Veil Useless field
    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    email = models.EmailField()

    nickname = models.CharField(
        max_length=150,
    )
    isHost = models.BooleanField(default=False)

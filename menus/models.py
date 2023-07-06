from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from common.models import CommonModel


class Menu(CommonModel):
    class MenuTypeChoices(models.TextChoices):
        COFFEE = ("coffee", "커피")
        ADE = ("ade", "에이드")
        TEA = ("tea", "차")
        BREAD = ("bread", "빵")
        SNACK = ("snack", "스낵")
        DDUK = ("dduk", "떡")

    name = models.CharField(
        max_length=50,
    )
    description = models.TextField()
    price = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
        ]
    )
    type = models.CharField(
        max_length=12,
        choices=MenuTypeChoices.choices,
    )
    image = models.URLField(
        null=True,
        blank=True,
    )
    cafes = models.ManyToManyField("cafes.Cafe")

    def __str__(self):
        return self.name


class AddOn(models.Model):
    name = models.CharField(
        max_length=50,
    )
    description = models.TextField()
    price = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
        ]
    )
    menus = models.ManyToManyField("menus.Menu")
    image = models.URLField(
        null=True,
        blank=True,
    )

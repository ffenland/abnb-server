from django.db import models
from django.conf import settings
from common.models import CommonModel


# Create your models here.
class Experience(CommonModel):
    """experience model"""

    name = models.CharField(
        max_length=50,
    )
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    address = models.CharField(
        max_length=80,
    )
    price = models.PositiveIntegerField()
    start_at = models.TimeField()
    end_at = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField("experiences.Perk")
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name


class Perk(CommonModel):
    """What included on Experience"""

    name = models.CharField(
        max_length=50,
    )
    details = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

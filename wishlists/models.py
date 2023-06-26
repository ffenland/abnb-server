from django.db import models
from common.models import CommonModel
from django.conf import settings

# Create your models here.


class Wishlist(CommonModel):
    """Wishlist model definition"""

    name = models.CharField(
        max_length=30,
    )
    cafes = models.ManyToManyField(
        "cafes.Cafe",
        blank=True,
    )
    experiences = models.ManyToManyField(
        "experiences.Experience",
        blank=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

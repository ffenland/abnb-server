from django.db import models
from common.models import CommonModel


# Create your models here.
class Category(CommonModel):
    """Cafe or Experience Category"""

    class CategoryKindChoices(models.TextChoices):
        CAFE = ("cafes", "For Cafes")
        EXPERIENCE = "experiencies", "For Experiencies"

    name = models.CharField(
        max_length=30,
    )
    kind = models.CharField(
        max_length=12,
        choices=CategoryKindChoices.choices,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

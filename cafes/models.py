from django.db import models
from django.conf import settings
from common.models import CommonModel


# Create your models here.
class Cafe(CommonModel):
    """Cafe model"""

    class CafeKindChoices(models.TextChoices):
        INDOOR = ("inddor", "실내")
        OUTDOOR = ("outdoor", "실외")
        BOTHDOOR = ("both", "실내외")
        TAKEOUT = "takeout", "포장전용"

    name = models.CharField(
        max_length=30,
    )
    address = models.CharField(
        max_length=80,
    )
    detail_address = models.CharField(
        max_length=50,
    )
    description = models.TextField()
    pet_allowed = models.BooleanField(
        default=False,
    )
    kind = models.CharField(
        max_length=20,
        choices=CafeKindChoices.choices,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    facilities = models.ManyToManyField(
        "cafes.Facility",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name

    def total_facilities(self):
        return self.facilities.count()

    def rating(self):
        count = self.review_set.count()
        if count == 0:
            return "None"
        else:
            total_rating = 0
            for review in self.review_set.all().values("rating"):
                total_rating += review["rating"]
            return round(total_rating / count, 2)


class Facility(CommonModel):
    """Cafe Facility Definition"""

    name = models.CharField(
        max_length=20,
    )
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Facilities"

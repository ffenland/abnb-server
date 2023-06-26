from django.db import models
from common.models import CommonModel

# Create your models here.


class Photo(CommonModel):
    file = models.ImageField()
    cf_id = models.CharField(
        max_length=140,
    )
    description = models.CharField(
        max_length=140,
    )
    cafe = models.ForeignKey(
        "cafes.Cafe",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "Photo File"


class Video(CommonModel):
    file = models.FileField()
    cf_id = models.CharField(
        max_length=140,
    )
    description = models.CharField(
        max_length=140,
    )
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "Video File"

from django.db import models
from django.conf import settings

# Create your models here.


class Cafe(models.Model):

    """카페 모델 테스트용"""

    name = models.CharField(max_length=50)
    score = models.PositiveIntegerField()
    description = models.TextField()
    addr_sido = models.CharField(max_length=9, verbose_name="시도")
    addr_sgg = models.CharField(max_length=9, verbose_name="시군구")
    addr_umd = models.CharField(max_length=5, verbose_name="읍면동")
    pets_allowed = models.BooleanField(default=False)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

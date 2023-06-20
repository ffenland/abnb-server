from django.db import models

# Create your models here.


class Cafe(models.Model):

    """카페 모델 테스트용"""

    name = models.CharField(max_length=50)
    score = models.PositiveIntegerField()
    description = models.TextField()
    addr_sido = models.CharField(max_length=9)
    addr_sgg = models.CharField(max_length=9)
    addr_umd = models.CharField(max_length=5)

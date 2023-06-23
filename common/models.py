from django.db import models


class CommonModel(models.Model):

    """Common Model"""

    created_at = models.DateTimeField(
        verbose_name="만든날짜",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="변경날짜",
        auto_now=True,
    )

    # do not make Database Table
    class Meta:
        abstract = True

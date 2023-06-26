from django.db import models
from django.conf import settings
from common.models import CommonModel

# Create your models here.


class Room(CommonModel):
    """CHAT Room model definition"""

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
    )

    def __str__(self):
        return "Chatting Room"


class Message(CommonModel):
    """CHAT Message model definition"""

    text = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    room = models.ForeignKey(
        "direct_messages.Room",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user} says : {self.text}"

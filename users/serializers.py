from rest_framework.serializers import ModelSerializer
from .models import User


class TinyUserSerializer(ModelSerializer):
    """For CafeDetail"""

    class Meta:
        model = User
        fields = (
            "nickname",
            "avatar",
        )

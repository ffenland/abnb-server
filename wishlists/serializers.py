from rest_framework.serializers import ModelSerializer
from cafes.serializers import CafeListSerializer
from .models import Wishlist


class WishlistsSerializer(ModelSerializer):
    cafes = CafeListSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Wishlist
        fields = ("name", "cafes")

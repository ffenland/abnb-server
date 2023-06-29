from rest_framework.serializers import ModelSerializer
from .models import Facility, Cafe
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class FacilitySerializer(ModelSerializer):
    class Meta:
        model = Facility
        fields = (
            "name",
            "description",
        )


class CafeListSerializer(ModelSerializer):
    class Meta:
        model = Cafe
        fields = (
            "pk",
            "name",
            "address",
            "category",
        )


class CafeDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer(
        read_only=True,
    )
    facilities = FacilitySerializer(
        many=True,
        read_only=True,
    )
    category = CategorySerializer(
        read_only=True,
    )

    class Meta:
        model = Cafe
        fields = "__all__"

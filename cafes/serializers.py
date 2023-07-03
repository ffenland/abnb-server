from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Facility, Cafe
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer


class FacilitySerializer(ModelSerializer):
    class Meta:
        model = Facility
        fields = (
            "name",
            "description",
        )


class CafeListSerializer(ModelSerializer):
    is_owner = SerializerMethodField(
        read_only=True,
    )
    photo_set = PhotoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Cafe
        fields = (
            "pk",
            "name",
            "address",
            "category",
            "is_owner",
            "photo_set",
        )

    def get_is_owner(self, cafe):
        request = self.context["request"]
        return cafe.owner == request.user


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
    potato = SerializerMethodField()
    is_owner = SerializerMethodField()
    photo_set = PhotoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Cafe
        fields = "__all__"

    def get_potato(self, cafe):
        # cafe = instance one model ok?
        return f"{cafe.name}result of Method"

    def get_is_owner(self, cafe):
        request = self.context["request"]
        return request.user == cafe.owner

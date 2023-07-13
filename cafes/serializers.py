from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Facility, Cafe
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class FacilitySerializer(ModelSerializer):
    class Meta:
        model = Facility
        fields = (
            "pk",
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


# Serializer에게 requst의 정보를 context 파라미터를 통해 수동으로 넘겨준다.


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
    is_on_wishlist = SerializerMethodField()
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
        if request:
            return request.user == cafe.owner
        else:
            return False

    def get_is_on_wishlist(self, cafe):
        request = self.context["request"]
        # 우선 현재 로그인된 유저의 Wishlist 중에
        # 현재 보고있는 cafe가 있는지 확인한다.
        # 그럼 wishlist는 여러개 일 수 있는거네?
        # mtm 관계니까

        if request:
            # 로그인하지 않은경우 False 반환
            if request.user.is_authenticated:
                return Wishlist.objects.filter(
                    user=request.user,
                    cafes__id=cafe.id,
                ).exists()
            else:
                return False
        else:
            return False

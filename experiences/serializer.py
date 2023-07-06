from rest_framework.serializers import ModelSerializer, SerializerMethodField
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from .models import Perk, Experience
from wishlists.models import Wishlist


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceListSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class ExperienceDetailSerializer(ModelSerializer):
    host = TinyUserSerializer(
        read_only=True,
    )

    perks = PerkSerializer(
        many=True,
        read_only=True,
    )
    category = CategorySerializer(
        read_only=True,
    )
    is_host = SerializerMethodField()
    is_on_wishlist = SerializerMethodField()

    class Meta:
        model = Experience
        fields = "__all__"

    def get_is_host(self, exp):
        request = self.context["request"]
        return request.user == exp.host

    def get_is_on_wishlist(self, exp):
        request = self.context["request"]
        # 우선 현재 로그인된 유저의 Wishlist 중에
        # 현재 보고있는 cafe가 있는지 확인한다.
        # 그럼 wishlist는 여러개 일 수 있는거네?
        # mtm 관계니까
        return Wishlist.objects.filter(
            user=request.user,
            experiences__id=exp.id,
        ).exists()

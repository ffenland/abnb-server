from rest_framework.serializers import ModelSerializer
from .models import Facility


class FacilitySerializer(ModelSerializer):
    class Meta:
        model = Facility
        fields = "__all__"

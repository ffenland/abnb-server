from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # exclude = ("created_at",)
        fields = (
            "pk",
            "name",
            "kind",
        )


class Old_CategorySerializer(serializers.Serializer):
    pk = serializers.IntegerField(
        read_only=True,
    )
    name = serializers.CharField(
        required=True,
        max_length=50,
    )
    kind = serializers.ChoiceField(
        choices=Category.CategoryKindChoices.choices,
    )
    created_at = serializers.DateTimeField(
        read_only=True,
    )

    def create(self, validated_data):
        return Category.objects.create(
            # name = validated_data["name"]
            # kind = validated_data["kind"]
            # don't use this else use **
            **validated_data
        )

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.kind = validated_data.get("kind", instance.kind)
        instance.save()
        return instance

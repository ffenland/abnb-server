from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "start_date",
            "end_date",
            "experience_time",
            "guests",
        )


class CreateCafeBookingSerializer(serializers.ModelSerializer):
    # Model에서는 nullable값이지만 여기서는 required로
    # 설정해준다.
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "start_date",
            "end_date",
            "guests",
        )

    def validate_start_date(self, value):
        now = timezone.localdate(timezone.now())
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")

        return value

    def validate_end_date(self, value):
        now = timezone.localdate(timezone.now())
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate(self, attrs):
        if attrs["end_date"] <= attrs["start_date"]:
            raise serializers.ValidationError(
                "The start date cannot be earlier than the end date."
            )
        if Booking.objects.filter(
            start_date__lte=attrs["end_date"],
            end_date__gte=attrs["start_date"],
        ).exists():
            raise serializers.ValidationError("those dates are already booked")

        return attrs

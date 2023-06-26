from django.contrib import admin
from .models import Booking

# Register your models here.


@admin.register(Booking)
class Booking(admin.ModelAdmin):
    list_display = (
        "kind",
        "user",
        "cafe",
        "experience",
        "start_date",
        "end_date",
        "experience_time",
        "guests",
    )

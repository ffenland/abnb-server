from django.contrib import admin
from .models import Cafe, Facility

# Register your models here.


@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "address",
        "kind",
        "owner",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "kind",
        "address",
        "facilities",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )

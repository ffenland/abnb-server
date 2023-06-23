from django.contrib import admin
from .models import Cafe, Facility
from categories.models import Category

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

    def get_form(self, request, obj=None, **kwargs):
        form = super(CafeAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["category"].queryset = Category.objects.filter(kind="cafes")
        return form


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

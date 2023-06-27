from django.contrib import admin
from .models import Cafe, Facility
from categories.models import Category

# Register your models here.


@admin.action(description="Set all addrss to none")
def reset_address(model_admin, request, querysets):
    """Admin method"""
    # 3 parameters is necessary
    for cafe in querysets.all():
        cafe.address = ""
        cafe.save()


@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    actions = (reset_address,)

    list_display = (
        "name",
        "address",
        "kind",
        "total_facilities",
        "owner",
        "rating",
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

    search_fields = (
        "name",
        "=rating",
        "^owner__username",
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

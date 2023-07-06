from django.contrib import admin
from .models import Menu, AddOn


# Register your models here.
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass


@admin.register(AddOn)
class AddOnAdmin(admin.ModelAdmin):
    pass

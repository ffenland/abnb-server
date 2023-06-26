from django.contrib import admin
from .models import Room, Message

# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "text",
        "room",
        "created_at",
    )
    list_filter = ("room", "created_at")

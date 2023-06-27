from collections.abc import Iterable
from typing import Any
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Review


class WordFilter(admin.SimpleListFilter):
    title = "Filter by words"
    parameter_name = "word"

    def lookups(
        self, request: HttpRequest, model_admin: ModelAdmin
    ) -> Iterable[tuple[Any, str]] | None:
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request: HttpRequest, reviews: QuerySet) -> QuerySet | None:
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            return reviews


class GoodOrBad(admin.SimpleListFilter):
    title = "Good or Bad"
    parameter_name = "isGood"

    def lookups(
        self, request: HttpRequest, model_admin: ModelAdmin
    ) -> Iterable[tuple[Any, str]] | None:
        return [
            ("good", "Good"),
            ("bad", "Bad"),
        ]

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None:
        isGood = self.value()
        if isGood:
            if isGood == "good":
                return queryset.filter(rating__gte=3)
            else:
                # isGood == bad
                return queryset.filter(rating__lt=3)
        else:
            return queryset


# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
        "rating",
    )
    list_filter = (
        WordFilter,
        GoodOrBad,
        "rating",
        "cafe__kind",
    )

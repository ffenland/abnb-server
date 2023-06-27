from django.urls import path
from . import views

urlpatterns = [
    path("", views.see_all_cafes),
    path("<str:cafe_id>", views.see_one_cafe),
]

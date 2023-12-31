from django.urls import path
from .views import Wishlists, WishlistDetail, WishlistToggle

urlpatterns = [
    path("", Wishlists.as_view()),
    path("<int:pk>", WishlistDetail.as_view()),
    path("<int:pk>/cafes/<int:cafe_pk>", WishlistToggle.as_view()),
]

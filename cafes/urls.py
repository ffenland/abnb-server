from django.urls import path
from . import views

urlpatterns = [
    path("", views.Cafes.as_view()),
    path("<int:pk>", views.CafeDetail.as_view()),
    path("<int:pk>/reviews/", views.CafeReviews.as_view()),
    path("<int:pk>/facilities/", views.CafeFacilities.as_view()),
    path("<int:pk>/photos/", views.CafePhotos.as_view()),
    path("facilities/", views.Facilities.as_view()),
    path("facilities/<int:pk>", views.FacilityDetail.as_view()),
]

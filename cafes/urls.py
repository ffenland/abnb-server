from django.urls import path
from . import views

urlpatterns = [
    path("facilities/", views.Facilities.as_view()),
    path("facilities/<int:pk>", views.FacilityDetail.as_view()),
]

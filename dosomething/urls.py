from django.urls import path
from .views import TestOne

urlpatterns = [(path("", TestOne.as_view()))]

from django.shortcuts import render
from django.http import HttpResponse
from .models import Cafe

# Create your views here.


def say_hello(request):
    return HttpResponse("Hello world.")


def see_all_cafes(request):
    cafes = Cafe.objects.all()
    return


def see_one_cafe(request, cafe_id):
    return

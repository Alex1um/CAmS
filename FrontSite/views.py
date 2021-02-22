from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from django.core.exceptions import ObjectDoesNotExist


def test(request):
    return render(request, "bars.html")


def test1(request):
    return render(request, "themes\\theme-one.html")

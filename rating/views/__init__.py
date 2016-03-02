from django.shortcuts import render
from django.http import HttpResponse
#from rating.views.rating import russian_artists, foreign_artists


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")



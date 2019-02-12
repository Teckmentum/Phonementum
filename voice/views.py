from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def incall_lobby(request):
    return HttpResponse("hola es una prueba de que se puede acceder")
"""URLS para voice/*

Todos los urls relacionados con el voice app estan declarados aqui.


Notes
-----
    Autor: Glorimar Castro-Noriega
    Creado: Febrero-12-2019

"""

"""URL para el app de Voice
"""
from django.contrib import admin
from django.urls import path
from hermes import views

urlpatterns = [
    # path('', views.greetings),
    path('greetings', views.greetings),
    path('voice_call_gather', views.incoming_voice_call_gather),
    path('incoming_voice_call_lobby', views.incoming_voice_call_lobby)
]


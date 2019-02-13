"""URLS para voice/*

Todos los urls relacionados con el voice app estan declarados aqui.


Notes
-----
    Autor: Glorimar Castro-Noriega
    Creado: Febrero-12-2019

"""


from django.contrib import admin
from django.urls import path

from voice import views

urlpatterns = [
    path('lobby/', views.incall_lobby), #path completo voice/lobby
    path('lobby', views.incall_lobby),
    path('department/', views.incall_department),
    path('department', views.incall_department),
    path('enqueue_call/<str:workspace>/<str:workflow>/<str:task>', views.enqueue_call),
    path('', views.index)


]


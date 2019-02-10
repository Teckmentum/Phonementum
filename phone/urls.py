"""URLS para phone/*

Todos los urls relacionados con el phone app estan declarados aqui.


Notes
-----
    Autor: Glorimar Castro-Noriega
    Creado: Febrero-8-2019

"""


from django.contrib import admin
from django.urls import include,path
import phone.views as views



urlpatterns = [
    #path('phone/', include('phone.urls'))  #incluye todos los url dentro del app phone
    path('makecall/', views.make_call())
]

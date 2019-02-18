from django.urls import path

from txt import views

urlpatterns = [
    path('test', views.test),
    path('', views.test)



]


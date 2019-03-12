"""phosrv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path

from phosrv import views_test
import voice.views as v_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views_test.index),
    path('hermes/', include('hermes.urls')),
    #path('assignment_callback',v_views.assignment_callback),
    #path('create_task', v_views.create_task),
    #path('accept_reservation', v_views.accept_reservation),
    path('txt/', include('txt.urls'))
]

from django.urls import path

from txt import views
from txt import test_receive
from txt import test_mms

urlpatterns = [
    path('test', views.test),
    path('', views.test),
    path('textrep',test_receive.sms_reply),
    path('testmms', test_mms)
]


"""views for debugging and srv test

"""
from django.http import HttpResponse

def index(request):
    return HttpResponse("Srv up and running")
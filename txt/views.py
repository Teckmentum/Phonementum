from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


from django.shortcuts import render

# Create your views here.
@csrf_exempt
def test(request):
    return HttpResponse("txt app working")
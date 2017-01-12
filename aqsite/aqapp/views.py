from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from .tasks import update_openaq_data

# Create your views here.

def index(request):
    context = {}
    update_openaq_data.delay()
    return render(request, 'aqapp/index.html', context)


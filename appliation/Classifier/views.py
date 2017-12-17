from django.shortcuts import render
from django.http import HttpResponse
from Classifier.models import Image
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    return render(
        request,
        'index.html'
    )

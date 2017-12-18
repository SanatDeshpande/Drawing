from django.shortcuts import render, redirect
from django.http import HttpResponse
from Classifier.models import Image, ImageClassifier
from django.views.decorators.csrf import csrf_exempt
import torch
from torch import autograd
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
import os
import pickle
import json

@csrf_exempt
def index(request, prediction=None):
    return render(
        request,
        'index.html'
    )

@csrf_exempt
def classify(request):
    image = Image.bytes_to_np(request.body, Image.HEIGHT, Image.WIDTH)
    with open('image', 'wb') as f:
        pickle.dump(image, f)
    prediction = ImageClassifier.make_prediction(image)
    print(prediction)
    return HttpResponse(status=200)

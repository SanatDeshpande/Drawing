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
def index(request):
    label = ImageClassifier.prediction
    if label is not None:
        return render(
            request,
            'index.html',
            {'predictedLabel': label}
        )
    return render(
        request,
        'index.html',
        {'predictedLabel': ''}
    )

@csrf_exempt
def classify(request):
    Image.image = Image.bytes_to_np(request.body, Image.HEIGHT, Image.WIDTH)
    ImageClassifier.prediction = ImageClassifier.make_prediction(Image.image)
    print(ImageClassifier.prediction)
    return redirect('index')

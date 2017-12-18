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
    #grabs predicted label if not None, and updates template
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
    #processes image into 26x26
    Image.image = Image.bytes_to_np(request.body, Image.HEIGHT, Image.WIDTH)

    #passes image through CNN to classify
    ImageClassifier.prediction = ImageClassifier.make_prediction(Image.image)

    #redirect to index for display...not sure what the best practice is here
    return redirect('index')

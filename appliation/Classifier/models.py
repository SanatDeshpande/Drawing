from django.db import models
import numpy as np
import torch
from torch import autograd
import torch.nn.functional as F
from torch.autograd import Variable
import pickle
import os

class Image(models.Model):
    #fixed dimensions for classifier
    HEIGHT, WIDTH = 26, 26

    #converts bytes from POST request to np float array
    def bytes_to_np(image, height, width):
        #converts to string array to make parsing easier
        image = str(image)[2:-1].split(',')
        image = [float(i) for i in image]
        return np.asarray(image, dtype=float).reshape(height, width)


class ImageClassifier(models.Model):
    class Classifier(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.HEIGHT, self.WIDTH = 26, 26
            self.conv1 = torch.nn.Conv2d(1, 16, kernel_size=3, stride=1)
            self.conv2 = torch.nn.Conv2d(16, 32, kernel_size=3, stride=1)
            self.final_conv = torch.nn.Conv2d(32, 8, kernel_size=1)
            self.linear1 = torch.nn.Linear(8, 6)
            self.linear2 = torch.nn.Linear(6, 5)
        def forward(self, x):
            x = x.view(-1, self.HEIGHT, self.WIDTH).unsqueeze(1)
            x = F.relu(self.conv1(x))
            x = F.relu(self.conv2(x))
            n, c, h, w = x.size()
            x = F.avg_pool2d(x, kernel_size=[h, w]) #the avg pooling computes one output value out of the matrix                      \

            x = self.final_conv(x).view(-1, 8)
            x = F.relu(self.linear1(x))
            x = F.relu(self.linear2(x))
            #x.data = torch.t(x.data)                                                                                                 \

            return x
    def make_prediction(image):
        model = ImageClassifier.Classifier()
        model.load_state_dict(torch.load('static/learned_parameters/parameters'))
        x = autograd.Variable(torch.from_numpy(image.astype(np.float32)))
        prediction = model(x)
        #prediction = np.argmax(prediction.data.numpy())
        return prediction
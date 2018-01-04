from django.db import models
import numpy as np
import torch
from torch import autograd
import torch.nn.functional as F
from torch.autograd import Variable
import pickle
import os
import math

class Image(models.Model):
    #fixed dimensions for classifier
    HEIGHT, WIDTH = 26, 26
    image = None
    #converts bytes from POST request to np float array
    def bytes_to_np(image, height, width):
        #converts to square (26x26) of just relevant pixel values
        image = image[::4]
        side_length = int(math.sqrt(len(image)))

        #converts to pytorch variable to make shrinking image easier
        image = torch.Tensor(image)
        image = image.view(1, -1, side_length)
        image = Variable(image)

        #uses avg pool to shrink image appropriately, and then trims
        '''
        Would be better to do this step client side to avoid sending
        a large post request. Also better to do it in one step, avoiding
        trimming the image.
        '''
        image = F.avg_pool2d(image, kernel_size=[int(side_length/height), int(side_length/width)])
        
        #TODO: Fix downsizing so that we never need to trim

        #returns image if it is the right size
        if image.size()[1] == height and image.size()[2] == width:
            return image.data.numpy().reshape(height, width)

        #trims image...not ideal solution, not ideal implementation
        image = image.data.numpy()
        _, w, h = image.shape
        image = image.reshape(w, h)
        output = []
        for i in range(height):
            temp = []
            for j in range(width):
                temp.append(image[i][j])
            output.append(temp)
        output = np.asarray(output)
        #returns data shaped as 26x26
        return output


class ImageClassifier(models.Model):
    prediction = None

    '''
    CNN for classification. Passes through 3 conv layers, with average pooling
    after the first 2. Then 2 linear layers for classification.
    The parameters obtained came from training that can be seen in the root
    directory.
    '''
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
            #appropriately shapes data
            x = x.view(-1, self.HEIGHT, self.WIDTH).unsqueeze(1)
            x = F.relu(self.conv1(x))
            x = F.relu(self.conv2(x))
            n, c, h, w = x.size()
            x = F.avg_pool2d(x, kernel_size=[h, w]) #the avg pooling computes one output value out of the matrix                      \

            #reshapes data for linear layers
            x = self.final_conv(x).view(-1, 8)
            x = F.relu(self.linear1(x))
            x = F.relu(self.linear2(x))

            return x

    def make_prediction(image):
        #initializes model as an instance of the CNN
        model = ImageClassifier.Classifier()
        BASE = os.path.dirname(os.path.realpath(__file__))
        #loads in learned parameters
        model.load_state_dict(torch.load(BASE + '/../static/learned_parameters/parameters'))

        #converts image to a pytorch variable and classifies it w/ forward pass
        x = autograd.Variable(torch.from_numpy(image.astype(np.float32)))
        prediction = model(x)
        prediction = np.argmax(prediction.data.numpy())

        #maps classification output to an English label
        name_map = {0: 'Apple', 1: 'Basketball', 2: 'Cookie', 3: 'Clock', 4: 'Fan'}

        return name_map[prediction]

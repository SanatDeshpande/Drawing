import numpy as np
import torch
from torch import autograd
import torch.nn.functional as F
from torch.autograd import Variable
import pickle
import sys

class ImageClassifier(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = torch.nn.Conv2d(1, 16, kernel_size=3, stride=1)
            self.conv2 = torch.nn.Conv2d(16, 32, kernel_size=3, stride=1)
            self.final_conv = torch.nn.Conv2d(32, 8, kernel_size=1)
            self.linear1 = torch.nn.Linear(8, 6)
            self.linear2 = torch.nn.Linear(6, 5)
        def forward(self, x):
            x = x.view(-1, HEIGHT, WIDTH).unsqueeze(1)
            x = F.relu(self.conv1(x))
            x = F.relu(self.conv2(x))
            n, c, h, w = x.size()
            x = F.avg_pool2d(x, kernel_size=[h, w]) #the avg pooling computes one output value out of the matrix
            x = self.final_conv(x).view(-1, NUM_CLASSES+3)
            x = F.relu(self.linear1(x))
            x = F.relu(self.linear2(x))
            #x.data = torch.t(x.data)
            return x

#loads data and splits into training and validation
images = np.load(sys.argv[1])
labels = np.load(sys.argv[2])

HEIGHT = len(images[0])
WIDTH = len(images[0][0])

images = images.reshape(images.shape[0], images.shape[1] * images.shape[2])
train_images = images[:45000]
train_labels = labels[:45000]
val_images = images[45000:]
val_labels = labels[45000:]

NUM_CLASSES = 5

#setup model and optimizer
model = ImageClassifier()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

def train(batch_size):
    # model.train() puts our model in train mode, which can require different
    # behavior than eval mode (for example in the case of dropout).
    model.train()
    # i is is a 1-D array with shape [batch_size]
    i = np.random.choice(train_images.shape[0], size=batch_size, replace=False)
    x = autograd.Variable(torch.from_numpy(train_images[i].astype(np.float32)))
    y = autograd.Variable(torch.from_numpy(train_labels[i].astype(np.int)))
    optimizer.zero_grad()
    y_hat_ = model(x)
    loss = F.cross_entropy(y_hat_, y)
    loss.backward()
    optimizer.step()
    return loss.data[0]


def approx_train_accuracy():
    i = np.random.choice(train_images.shape[0], size=1000, replace=False)
    x = Variable(torch.from_numpy(train_images[i].astype(np.float32)))
    y = train_labels[i].astype(np.int)
    y_hat = []
    for example in x:
        y_hat.append(model(example).data.numpy()[0])
    return (np.argmax(y_hat, axis=1) == y).mean()

def val_accuracy():
    x = Variable(torch.from_numpy(val_images[:].astype(np.float32)))
    y = val_labels[:].astype(np.int)
    y_hat = []
    for example in x:
        y_hat.append(model(example).data.numpy()[0])
    return (np.argmax(y_hat, axis=1) == y).mean()


NUM_OPT_STEPS = 90000
plot_iterations = 10000
train_accs, val_accs = [], []
batch_size = 10
for i in range(NUM_OPT_STEPS):
    l = train(batch_size)
    if i % plot_iterations == 0:
        print(l)
        train_accs.append(approx_train_accuracy())
        val_accs.append(val_accuracy())
        print("%6d %5.2f %5.2f" % (i, train_accs[-1], val_accs[-1]))
        break
torch.save(model.state_dict(), './model')

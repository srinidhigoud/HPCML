
# coding: utf-8

# In[1]:

from __future__ import print_function
import os
from skimage import io, transform
import argparse
import torch
import torchvision
import pandas as pd
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from PIL import Image
from torchvision import datasets, transforms
from torch.autograd import Variable
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils


# In[2]:

batch_size = 100   # input batch size for training
epochs = 5       # number of epochs to train
lr = 0.01
num_inputs_1 = 3072
num_outputs_1 = 1024
num_outputs_2 = 256
num_outputs_3 = 17



# In[8]:

class data(Dataset):

    def __init__(self, csv_file, root_dir, transform=None):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.file = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.file)

    def __getitem__(self, idx):
        img_name = os.path.join(self.root_dir,
                                self.file.iloc[idx, 0])
        image = Image.open(img_name+'.jpg')
        image = image.convert('RGB')
#         image = io.imread()
#         image = Image.fromarray(image.numpy(), mode='L')
        if self.transform is not None:
            image = self.transform(image)
        labels = self.file.iloc[idx, 1].astype('int')

        

        return (image,labels)


# In[9]:

data_transform = transforms.Compose([
    transforms.Resize((32,32)),
    transforms.ToTensor()
])
train_dataset = data(csv_file='CSCI-GA.3033-023/kaggleamazon/train.csv', root_dir='CSCI-GA.3033-023/kaggleamazon/train-jpg/',transform = data_transform)
print(train_dataset[0])
train_loader = DataLoader(train_dataset,batch_size, num_workers=1)
test_dataset = data(csv_file='CSCI-GA.3033-023/kaggleamazon/test.csv', root_dir='CSCI-GA.3033-023/kaggleamazon/train-jpg/',transform = data_transform)
test_loader = DataLoader(test_dataset, batch_size,  num_workers=1)






# In[10]:

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.linear1 = nn.Linear(num_inputs_1, num_outputs_1)
        self.linear2 = nn.Linear(num_outputs_1, num_outputs_2)
        self.linear3 = nn.Linear(num_outputs_2, num_outputs_3)

    def forward(self, input):
        input = input.view(-1, num_inputs_1) # reshape input to batch x num_inputs
        z = F.relu(self.linear1(input))
        z = F.relu(self.linear2(z))
        output = F.log_softmax(self.linear3(z))
        return output
net = Net()
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=lr, momentum = 0.9)


# In[11]:

def train(epoch, break_val):
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = Variable(data), Variable(target)
        optimizer.zero_grad()
        output = net(data)
        loss = criterion(output, target)
        print(batch_idx, loss.data[0])
        loss.backward()
        optimizer.step()
        if batch_idx==break_val:
            return
        if batch_idx % 100 == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.data[0]))



# In[12]:

for epoch in range(1, epochs + 1):
    train(epoch,500)


# In[ ]:




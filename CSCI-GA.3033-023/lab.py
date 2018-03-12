from __future__ import print_function
import sys
import os
import torch
import torchvision
import pandas as pd
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from PIL import Image
from torchvision import datasets
from torch.autograd import Variable
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import time

n = 1
batch_size = 100   # input batch size for training
epochs = 5       # number of epochs to train
lr = 0.01
num_inputs_1 = 3072
num_outputs_1 = 1024
num_outputs_2 = 256
num_outputs_3 = 17
agg_io_time = 0
agg_pre_time = 0
agg_waiting_time = 0
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
        t11 = time.monotonic()
        image = Image.open(img_name+'.jpg')
        t12 = time.monotonic()-t11
        t21 = time.monotonic()
        image = image.convert('RGB')
        if self.transform is not None:
            image = self.transform(image)
        t22 = time.monotonic()-t21
        labels = self.file.iloc[idx, 1].astype('int')

        

        return (t12,t22,image,labels)
data_transform = transforms.Compose([
    transforms.Resize((32,32)),
    transforms.ToTensor()
])
train_dataset = data(csv_file='kaggleamazon/train.csv', root_dir='kaggleamazon/train-jpg/',transform = data_transform)
#agg_waiting_time = time.monotonic()
train_loader = DataLoader(train_dataset,batch_size, num_workers=n)
#agg_waiting_time = time.monotonic() - agg_waiting_time
test_dataset = data(csv_file='kaggleamazon/test.csv', root_dir='kaggleamazon/train-jpg/',transform = data_transform)
test_loader = DataLoader(test_dataset, batch_size,  num_workers=n)
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


def train(epoch,agg_io_t,agg_pre_t,agg_waiting_t):
    waiting_time1 = time.monotonic()
    for batch_idx, (tio,tpre,data, target) in enumerate(train_loader):
        waiting_time = time.monotonic()-waiting_time1
        agg_io_t += sum(tio)
        agg_pre_t += sum(tpre)
        agg_waiting_t += waiting_time 
        data, target = Variable(data), Variable(target)
        optimizer.zero_grad()
        output = net(data)
        loss = criterion(output, target)
        #print(batch_idx, loss.data[0])
        loss.backward()
        # optimizer.step()
        # if batch_idx % 100000 == 0:
        #     print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
        #         epoch, batch_idx * len(data), len(train_loader.dataset),
        #         100. * batch_idx / len(train_loader), loss.data[0]))
        waiting_time1 = time.monotonic()
    return (agg_io_t,agg_pre_t,agg_waiting_t)

for epoch in range(1, epochs + 1):
    (t1,t2,t3) = train(epoch,agg_io_time,agg_pre_time,agg_waiting_time)
#     print(t1)
    #print(".............")
    agg_io_time += t1 
    agg_pre_time += t2

    agg_waiting_time += t3
    #print(agg_io_time,agg_pre_time,agg_waiting_time)
    #print(".............")
print(n,agg_io_time,agg_pre_time,agg_waiting_time)
print(".............")


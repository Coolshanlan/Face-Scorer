# %%
import ResNet
import torch
import pandas as pd
from pandas import DataFrame
from torch import nn
from PIL import Image
import numpy as np
import random
from torch import tensor
import torch.optim as optim
import torch.nn.functional as F
import os
from math import ceil
import gc
from TrainDataloader import TrainDataset
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, utils
# %%

trainImagePath = []
trainImageLabel = []
image_size = 224
learning_rate = 0.001
batchsize = 10
trainDataLoader=None
trainloader = None
trans=None
def updateData():
    global trainImagePath, trainImageLabel, trainloader, trans
    try:
        traincsv = pd.read_csv(os.path.dirname(os.path.abspath(__file__))+"\\train.csv", header=None,engine='python')
        trainImagePath = [("dataset/"+str(i)) for i in traincsv[0]]
        trainImageLabel = torch.LongTensor(np.array(traincsv[1]))
        normalize = transforms.Normalize(mean=[0.5, 0.5, 0.5],
                                 std=[0.229, 0.224, 0.225])
        trans = transforms.Compose([transforms.ToTensor(), transforms.ToPILImage(), transforms.Resize((image_size, image_size)),
                                    transforms.ToTensor(), normalize])
        trainDataLoader = TrainDataset(
        trainImagePath, trainImageLabel, transformer=trans)
        trainloader = DataLoader(trainDataLoader, batch_size=batchsize, shuffle=True)
    except:
        trainImagePath=[]
        trainImageLabel=[]

def prediction(img):
    img = trans(img)
    img = img[None, :, :, :]
    model.eval()
    output = model(img)[:,0]
    #output = F.softmax(F.sigmoid(output))
    # sum = 0.0
    # for j in range(0, len(output)):
    #     for i in range(0, len(output[j])):
    #         sum += i*output[j][i].item()
    return output.item()


def train():
    global model, trainloader, lossfunc
    lossvalue = 0
    acc = 0
    model.train()
    for (img, label) in trainloader:
        output = model(img)[:,0]
        loss = lossfunc(output, label.float())
        print(loss)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    model.eval()
    with torch.no_grad():
        for (img, label) in trainloader:
            output = model(img)[:,0]
            loss = lossfunc(output, label.float())
            lossvalue += loss.detach().item()
            # for i in range(0, len(output)):
            #     if output[i].argmax() == label[i]:
            #         acc += 1
    torch.save(model.state_dict(), "Resnow.pkl")
    return lossvalue/(len(trainloader))#acc/len(trainImageLabel), lossvalue/(len(trainloader))


updateData()
# transforms.ColorJitter(brightness=0.3, contrast=0.3),

model = ResNet.ResNet(1, [3, 4, 6, 4], insize=image_size,num_classes=1)
if os.path.isfile("Resnow.pkl"):
    model.load_state_dict(torch.load("Resnow.pkl"))
lossfunc = torch.nn.MSELoss()
optimizer = torch.optim.Adam(
    model.parameters(), lr=learning_rate)
# for i in range(0, 20):
#     lossv, accv = train()
#     print(lossv, accv)

import os # 换cuda的时候不小心下了TensorFlow,所以暂时这样吧
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # 允许重复加载OpenMP 库（规避报错）
os.environ["OMP_NUM_THREADS"] = "4" 

import random
import numpy as np

import torch
from torch import nn,optim
from torch.utils.data import DataLoader
from torchvision import datasets , transforms
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题


#---------------------------数据预处理--------------------------

transform = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize((0.1307),(0.3081))
    ]
)

train_dataset = datasets.MNIST(root="./data",download=True,train=True,transform=transform)
test_dataset = datasets.MNIST(root="./data", train=False, download=True, transform=transform)

train_loader = DataLoader(train_dataset,batch_size=64)
test_dataset = DataLoader(test_dataset,batch_size=1000,shuffle=False)




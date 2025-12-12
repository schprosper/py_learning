import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
torch.manual_seed(42)
d32 = torch.float32
d16 = torch.float16

# In [1]
x1 = 2.0 / 10000
print(f"{x1: .18f}")  # print 18 digits to the right of decimal point

# In [2]
x2 = 1 + (1/10000) - (1 - 1/10000)
print(f"{x2: .18f}")
'''
实现一个 “10 分类任务”：输入是 20 维特征
输出是 10 个类别的分类结果。
先以数值不稳定的次等方法构建网络，
再用数值稳定的改进方案实现，并对比差异。
'''
# 步骤1 准备训练数据，随机生成数据
X_train = torch.randn((100,20),dtype=d32)
y_train = torch.randint(0,10,(1000,)) # 【） so 10

# 构建神经网络——模型是一个对象
class Bad_Mutiple_Classfy_Model(nn.Module) :
    def __init__(self):
        super.__init__()

        self.layers = nn.Sequential(
            nn.Linear(20,25),
            nn.ReLU(),
            nn.Linear(25,15),
            nn.ReLU(),
            nn.Linear(15,10), # 这里，先得到线性的Liner
            nn.Softmax(dim = 1) # 按行计算 每行元素概率和为1
        )

    def forward(self,x) :
        return self.layers(x)
    


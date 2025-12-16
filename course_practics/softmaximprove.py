import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
torch.manual_seed(42)
d32 = torch.float32
d16 = torch.float16
lr = 0.01

# In [1]
x1 = 2.0 / 10000
print(f"{x1: .18f}")  # print 18 digits to the right of decimal point

# In [2]
x2 = 1 + (1/10000) - (1 - 1/10000)
print(f"{x2: .18f}")
'''s
实现一个 “10 分类任务”：输入是 20 维特征
输出是 10 个类别的分类结果。
先以数值不稳定的次等方法构建网络，
再用数值稳定的改进方案实现，并对比差异。
'''
# 步骤1 准备训练数据，随机生成数据
X_train = torch.randn((1000,20),dtype=d32)
y_train = torch.randint(0,10,(1000,),dtype=torch.long) # 【） so 10
# 1000个标签，long型（NLLLoss要求）

# 构建神经网络——模型是一个对象
class Bad_Mutiple_Classfy_Model(nn.Module) :
    def __init__(self):
        super().__init__() # super是函数，调用父类的方法的，需要用到父类的性质，所以父类也必须init化

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

model = Bad_Mutiple_Classfy_Model()  # 实例化调用
# 公式： w' = w - a * w * 梯度

criteria = nn.NLLLoss()
optimize = optim.SGD(model.parameters(),lr=0.01)

# 训练循环

for epoch in range (5):
    model.train()
    optimize.zero_grad() # 清零梯度
    y_train_pre= model(X_train)
    y_train_log = torch.log(y_train_pre) # 使用他的log跟随自动微分
    loss = criteria(y_train_log,y_train)
    loss.backward()
    optimize.step()
    print(f"循环{epoch+1},损失：{loss.item():.4f}")

 # ======================更好的模型的训练=========================


print("======================更好的模型的训练=========================")
class  GM(nn.Module):
    def __init__(self):
        super().__init__()

        self.layer = nn.Sequential(
            nn.Linear(20,25),
            nn.ReLU(),
            nn.Linear(25,15),
            nn.ReLU(),
            nn.Linear(15,10)

        )

    def forward(self,x):
        return self.layer(x)
    
Good_model = GM()
criteria = nn.CrossEntropyLoss()
optimizer = optim.SGD(Good_model.parameters(),lr=lr)

for epoch in range(5):
    Good_model.train()
    optimizer.zero_grad()
    y_pre = Good_model(X_train)
    loss = criteria(y_pre,y_train)
    loss.backward()
    optimizer.step()
    print(f"循环{epoch+1},损失：{loss.item():.4f}")

    


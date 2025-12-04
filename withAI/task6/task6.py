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




#------------参数调试---------------------------
dropout = 0.1 # 0.5 # 0.3 # 0.01
lr   = 0.001  # 1 
epochs = 2  # 训练轮次,其实1\2轮差距不是很大了,第二轮就开始震荡了
#-------------------- 数据预处理--------------------------------------
# 图像数据预处理
# transforms.Compose: 将多个数据变换操作组合成一个序列
# 类似与Sequence不过这里针对的是数据的处理
# 这里的数据集不是100的倍数,不过没关系


transform = transforms.Compose([
    transforms.ToTensor(),# 无需传入参数,因为他是统一标准,经过继承,他会直接继承到需要操作的图像数据的属性
    # 将PIL图像转换为张量，同时将像素值从[0,255]自动归一化到[0,1]
    # 原本的是(H, W, C),我们要求(C, H, W)
    transforms.Normalize((0.1307),(0.3081))# 行业标准,自己算的代码放在最下面
])


# 数据集处理,一直按照:先正确装载(包含转化),后划分的逻辑
train_dataset = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
test_dataset = datasets.MNIST(root="./data", train=False, download=True, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)  # 训练时打乱顺序避免模型学习到数据顺序
test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False)  # 测试时不需要打乱


# TODO: 定义CNN模型


class MyCNN(nn.Module):
    def __init__(self):
        super().__init__()
        # 针对每一个元数据,来看是多少d,通道数和batch是辅助的不算在几d里面
        # 普通非矩阵数据只是排列1d,矩阵数据(图片数据)2d,含有时间特征的视频是3d
        self.conv1 = nn.Conv2d(
            in_channels= 1, # 灰度图通道固定是1
            out_channels=16, # 16个卷积核来提取特征,16种特征
            kernel_size = 3, # 自动认为是矩形
            padding= 1 #防止数据丢失 
        )
        # 通道,卷积核,卷积核大小,缓解边缘信息丢失保持原大小不放缩
        
        # 卷积后: [batch_size, 16, 28, 28]


        # 第二个卷积块,继续特征提取

        self.conv2 = nn.Conv2d(
            in_channels=16,     
            out_channels=32,    
            kernel_size=3,      
            padding=1           
        )

        # 卷积后: [batch_size, 32, 14, 14]

        # 激活函数
        self.relu = nn.ReLU() # 解决梯度消失
        self.Sigmoid = nn.Sigmoid()

        #22最大池化
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        # 全连接层,回到我们的MPL了
        self.fc1 = nn.Linear(32 * 7 * 7, 128)  # 但是这里是自己算的,可能有通用的提取特征方法
        self.fc2 = nn.Linear(128, 10)

        # self.fcstep1 = nn.Linear(128,64)
        # self.fcstep2 = nn.Linear(64,32)
        # self.fcstep3 = nn.Linear(32,10)

        self.dropout = nn.Dropout(dropout)


    def forward(self,x):

        '''
        输入[bc,1,28,28]
        输出[bc,10]
        '''
        # 卷积块1,卷积之后紧接着池化一步,保证计算效率,并且因为数字识别过于简单,不需要多次卷积
        x = self.conv1(x)      # -> [batch_size, 16, 28, 28]
        x = self.relu(x)       # 激活函数，形状不变
        x = self.pool(x)       # 最大池化 -> [batch_size, 16, 14, 14]

        # 第二个卷积块  
        x = self.conv2(x)      # -> [batch_size, 32, 14, 14]
        x = self.relu(x)       # 激活函数
        x = self.pool(x)       # 最大池化 -> [batch_size, 32, 7, 7]

        # 展平操作:将多维特征图转换为一维向量，为全连接层准备
        x = x.view(-1, 32 * 7 * 7)


        # 全连接层
        x = self.fc1(x)        # 128
        x = self.relu(x)
        x = self.dropout(x)    # Dropout防止过拟合
        x = self.fc2(x)        # 10个类别的得分

        # x = self.Sigmoid(x)       
        # x = self.fcstep1(x)
        # x = self.Sigmoid(x) 
        # x = self.fcstep2(x)
        # x = self.Sigmoid(x) 
        # s = self.fcstep3(x)    
        return x
    

# TODO: model编写完成,开始定义训练和验证函数
'''对于每一批次:
换模式,数据转移,前向传播,计算损失,zero_gard梯度,loss.backward,优化step'''
def train(model, train_loader, criterion, optimizer, device):

    model.train() 

    total_loss = 0.0  # 累计损失
    total_samples = 0  # 总样本数


    for idx, (images, labels) in enumerate(train_loader):

        images, labels = images.to(device), labels.to(device)
        outputs = model(images)

        loss = criterion(outputs, labels)

        # 反向传播
        optimizer.zero_grad()  
        loss.backward()
        optimizer.step()
    
        # 累计统计
        batch_size = images.size(0)  # 当前批次样本数
        total_loss += loss.item() * batch_size  # 累计损失(乘以批次大小)
        # 之所以还原,是因为我们的数据集是938,大小并不一样
        # 这里的item,本身就是取的平均值.
        total_samples += batch_size  # 累计样本数
        
        # 每100个批次打印一次训练状态
        if idx % 100 == 0:
            print(f'  训练批次 [{idx}/{len(train_loader)}], 当前批次损失: {loss.item():.4f}')


            
    avg_loss = total_loss / total_samples
    return avg_loss

# 逻辑一样,定义验证函数,对于分类问题用正确率
def evaluate(model, test_loader, criterion, device):
    model.eval()  # 设置为评估模式，禁用dropout、使用训练好的batch normalization统计量
    total_loss = 0.0
    correct = 0    # 正确预测的样本数
    total_samples = 0
    
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            
            # 前向传播
            outputs = model(images)
            
            # 计算损失
            loss = criterion(outputs, labels)
            
            # 累计损失
            batch_size = images.size(0)
            total_loss += loss.item() * batch_size
            total_samples += batch_size
            
            # 计算准确率
            # torch.max返回(最大值, 最大值索引)，我们只需要索引(预测类别)
            _, predicted = torch.max(outputs.data, 1)  # 在维度1(类别维度)上取最大值
                         
            # 统计正确预测的数量
            correct += (predicted == labels).sum().item()  # .item()将张量转换为Python数值
    # 张量的逐元素比较逻辑，并不是 “矩阵等于矩阵” 的整体判断，而是
    #  “逐个样本对应比较”，最后统计正确的数量。返回的不是bools而是0和1
    # 计算平均损失和准确率
    avg_loss = total_loss / total_samples
    accuracy = 100.0 * correct / total_samples  # 转换为百分比
    
    return avg_loss, accuracy


if __name__ == "__main__" :
    # ---------------初始化-----------------------
    seed = 42  # 任意固定整数
    random.seed(seed)  # Python 原生随机数种子
    np.random.seed(seed)  # NumPy 随机数种子
    torch.manual_seed(seed)  # PyTorch CPU 随机数种子
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = MyCNN().to(device)
    # 概率问题交叉熵
    criterion = nn.CrossEntropyLoss() 
    # Adam优化器，自适应学习率
    optimizer = optim.Adam(model.parameters(), lr=lr) 
    train_losses = []
    test_losses = []
    test_accuracies = []


    # 训练循环
    for idx in range(epochs):
         print(f"\nEpoch [{idx+1}/{epochs}]")

         train_loss = train(model,train_loader,criterion ,optimizer,device)

         test_loss ,test_accuracy = evaluate(model,test_loader,criterion,device)

         train_losses.append(train_loss)
         test_losses.append(test_loss)
         test_accuracies.append(test_accuracy)


         print(f"Epoch [{idx+1}/{epochs}] 完成:")
         print(f"  训练损失: {train_loss:.4f}")
         print(f"  测试损失: {test_loss:.4f}") 
         print(f"  测试准确率: {test_accuracy:.2f}%")


    #---------------画图-----------------
    plt.figure(figsize=(15,5))
    # 子图1: 损失曲线
    plt.subplot(1,2,1)
    plt.plot(range(1, epochs+1), train_losses, 'b-', label='训练损失', linewidth=2)
    plt.plot(range(1, epochs+1), test_losses, 'r-', label='测试损失', linewidth=2)
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('Loss', fontsize=12)
    plt.title('训练和测试损失曲线', fontsize=14)


    # 子图2: 准确率曲线
    plt.subplot(1, 2, 2)
    plt.plot(range(1, epochs+1), test_accuracies, 'g-', label='测试准确率', linewidth=2)
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('准确率 (%)', fontsize=12)
    plt.title('测试准确率曲线', fontsize=14)

    plt.tight_layout()  # 自动调整子图间距
    plt.show()
    final_test_loss = test_losses[epochs -1]
    final_test_accuracy = test_accuracies[epochs -1]

    accuracy_gap = final_test_accuracy - final_test_accuracy
    print(f"终测准确率: {final_test_accuracy:.4f}%")
    print(f"终测损失: {final_test_loss:.4f}")
    print(f"训测准确率差值: {accuracy_gap:.4f}%")    

'''
from torchvision.datasets import MNIST

from torch.utils.data import DataLoader

# 1. 加载 MNIST 数据集（仅做 ToTensor 转换，不提前标准化）
dataset = MNIST(
    root="./data",
    train=True,  # 用训练集计算（数据量足够，统计更准确）
    download=True,
    transform=transforms.ToTensor()  # 只转 Tensor[0,255]→[0,1]），不标准化
)
dataloader = DataLoader(dataset, batch_size=128, shuffle=False)  # 无需shuffle，统计全局

# 2. 初始化统计变量（避免溢出，用 float64
total_pixels = 0  # 总像素数
sum_pixels = 0.0  # 所有像素值之和
sum_sq_pixels = 0.0  # 所有像素值的平方和

# 3. 遍历数据集，累积统计量
for images, _ in dataloader:
    # images shape: (batch_size, 1, 28, 28)
    batch_pixels = images.numel()  # 当前批次总像素数
    sum_pixels += images.sum().item()  # 累积像素和
    sum_sq_pixels += (images **2).sum().item()  # 累积像素平方和
    total_pixels += batch_pixels

# 4. 计算全局均值和标准差

mean = sum_pixels / total_pixels
std = (sum_sq_pixels / total_pixels - mean** 2) **0.5

print(f"自己计算的 MNIST 均值：{mean:.4f}")  
print(f"自己计算的 MNIST 标准差：{std:.4f}")  

# 5. 直接用自己计算的 mean/std 做标准化
from torchvision import transforms
transforms = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((mean,), (std,))  # 替换成自己算的结果
])
'''